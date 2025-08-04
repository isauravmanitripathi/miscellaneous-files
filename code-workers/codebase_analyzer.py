#!/usr/bin/env python3
"""
Codebase Merkle Tree Analyzer
Analyzes code structure, builds dependency graphs, and creates Merkle trees
for efficient change detection and impact analysis.
Exports results as markdown for AI analysis.
"""

import ast
import hashlib
import json
import os
import sys
import re
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Set, Optional, Any, Tuple
import argparse
from datetime import datetime


@dataclass
class CodeEntity:
    """Represents a code entity (function, class, variable)"""
    name: str
    type: str  # 'function', 'class', 'variable', 'import'
    file_path: str
    line_start: int
    line_end: int
    content_hash: str
    dependencies: List[str]  # What this entity depends on
    dependents: List[str]    # What depends on this entity
    parameters: List[str] = None
    return_type: str = None
    docstring: str = None


class CodeParser:
    """Parses multiple programming languages and extracts code entities and relationships"""
    
    def __init__(self):
        self.entities = {}
        self.file_imports = defaultdict(set)
        self.function_calls = defaultdict(set)
        self.variable_usage = defaultdict(set)
    
    def parse_file(self, file_path: str) -> Dict[str, CodeEntity]:
        """Parse a file based on its extension"""
        path = Path(file_path)
        extension = path.suffix.lower()
        
        if extension == '.py':
            return self._parse_python_file(file_path)
        elif extension == '.java':
            return self._parse_java_file(file_path)
        elif extension == '.kt':
            return self._parse_kotlin_file(file_path)
        elif extension == '.swift':
            return self._parse_swift_file(file_path)
        else:
            return {}
    
    def _parse_python_file(self, file_path: str) -> Dict[str, CodeEntity]:
        """Parse a Python file and extract all code entities"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            entities = {}
            
            # Extract imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        entity = self._create_import_entity(alias.name, file_path, node.lineno)
                        entities[f"import_{alias.name}"] = entity
                        self.file_imports[file_path].add(alias.name)
                
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        full_name = f"{module}.{alias.name}" if module else alias.name
                        entity = self._create_import_entity(full_name, file_path, node.lineno)
                        entities[f"import_{full_name}"] = entity
                        self.file_imports[file_path].add(full_name)
            
            # Extract classes and functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    entity = self._create_function_entity_python(node, file_path, content)
                    entities[f"func_{node.name}"] = entity
                    
                elif isinstance(node, ast.ClassDef):
                    entity = self._create_class_entity_python(node, file_path, content)
                    entities[f"class_{node.name}"] = entity
                
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            entity = self._create_variable_entity(target.id, file_path, node.lineno, content)
                            entities[f"var_{target.id}"] = entity
            
            # Analyze function calls and dependencies
            self._analyze_python_dependencies(tree, file_path, entities)
            
            return entities
            
        except Exception as e:
            print(f"Error parsing Python file {file_path}: {e}")
            return {}
    
    def _parse_java_file(self, file_path: str) -> Dict[str, CodeEntity]:
        """Parse a Java file using regex patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            entities = {}
            lines = content.split('\n')
            
            # Parse imports
            import_pattern = r'import\s+([\w\.]+);'
            for i, line in enumerate(lines):
                match = re.search(import_pattern, line)
                if match:
                    import_name = match.group(1)
                    entity = self._create_import_entity(import_name, file_path, i + 1)
                    entities[f"import_{import_name}"] = entity
            
            # Parse classes
            class_pattern = r'(?:public\s+|private\s+|protected\s+)?class\s+(\w+)'
            for i, line in enumerate(lines):
                match = re.search(class_pattern, line)
                if match:
                    class_name = match.group(1)
                    entity = self._create_class_entity_generic(class_name, file_path, i + 1, content)
                    entities[f"class_{class_name}"] = entity
            
            # Parse methods
            method_pattern = r'(?:public\s+|private\s+|protected\s+)?(?:static\s+)?[\w<>\[\]]+\s+(\w+)\s*\([^)]*\)\s*\{'
            for i, line in enumerate(lines):
                match = re.search(method_pattern, line)
                if match:
                    method_name = match.group(1)
                    if method_name not in ['if', 'for', 'while', 'switch']:  # Avoid control structures
                        entity = self._create_function_entity_generic(method_name, file_path, i + 1, content)
                        entities[f"func_{method_name}"] = entity
            
            return entities
            
        except Exception as e:
            print(f"Error parsing Java file {file_path}: {e}")
            return {}
    
    def _parse_kotlin_file(self, file_path: str) -> Dict[str, CodeEntity]:
        """Parse a Kotlin file using regex patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            entities = {}
            lines = content.split('\n')
            
            # Parse imports
            import_pattern = r'import\s+([\w\.]+)'
            for i, line in enumerate(lines):
                match = re.search(import_pattern, line)
                if match:
                    import_name = match.group(1)
                    entity = self._create_import_entity(import_name, file_path, i + 1)
                    entities[f"import_{import_name}"] = entity
            
            # Parse classes
            class_pattern = r'(?:data\s+)?class\s+(\w+)'
            for i, line in enumerate(lines):
                match = re.search(class_pattern, line)
                if match:
                    class_name = match.group(1)
                    entity = self._create_class_entity_generic(class_name, file_path, i + 1, content)
                    entities[f"class_{class_name}"] = entity
            
            # Parse functions
            function_pattern = r'fun\s+(\w+)\s*\([^)]*\)'
            for i, line in enumerate(lines):
                match = re.search(function_pattern, line)
                if match:
                    function_name = match.group(1)
                    entity = self._create_function_entity_generic(function_name, file_path, i + 1, content)
                    entities[f"func_{function_name}"] = entity
            
            return entities
            
        except Exception as e:
            print(f"Error parsing Kotlin file {file_path}: {e}")
            return {}
    
    def _parse_swift_file(self, file_path: str) -> Dict[str, CodeEntity]:
        """Parse a Swift file using regex patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            entities = {}
            lines = content.split('\n')
            
            # Parse imports
            import_pattern = r'import\s+(\w+)'
            for i, line in enumerate(lines):
                match = re.search(import_pattern, line)
                if match:
                    import_name = match.group(1)
                    entity = self._create_import_entity(import_name, file_path, i + 1)
                    entities[f"import_{import_name}"] = entity
            
            # Parse classes/structs
            class_pattern = r'(?:class|struct|enum)\s+(\w+)'
            for i, line in enumerate(lines):
                match = re.search(class_pattern, line)
                if match:
                    class_name = match.group(1)
                    entity = self._create_class_entity_generic(class_name, file_path, i + 1, content)
                    entities[f"class_{class_name}"] = entity
            
            # Parse functions
            function_pattern = r'func\s+(\w+)\s*\([^)]*\)'
            for i, line in enumerate(lines):
                match = re.search(function_pattern, line)
                if match:
                    function_name = match.group(1)
                    entity = self._create_function_entity_generic(function_name, file_path, i + 1, content)
                    entities[f"func_{function_name}"] = entity
            
            return entities
            
        except Exception as e:
            print(f"Error parsing Swift file {file_path}: {e}")
            return {}
    
    def _create_import_entity(self, name: str, file_path: str, line_no: int) -> CodeEntity:
        """Create import entity"""
        content_hash = self._hash_content(f"import {name}")
        return CodeEntity(
            name=name,
            type='import',
            file_path=file_path,
            line_start=line_no,
            line_end=line_no,
            content_hash=content_hash,
            dependencies=[],
            dependents=[]
        )
    
    def _create_function_entity_python(self, node: ast.FunctionDef, file_path: str, content: str) -> CodeEntity:
        """Create function entity for Python"""
        lines = content.split('\n')
        func_content = '\n'.join(lines[node.lineno-1:node.end_lineno])
        content_hash = self._hash_content(func_content)
        
        # Extract parameters
        parameters = [arg.arg for arg in node.args.args]
        
        # Extract docstring
        docstring = ast.get_docstring(node)
        
        return CodeEntity(
            name=node.name,
            type='function',
            file_path=file_path,
            line_start=node.lineno,
            line_end=node.end_lineno,
            content_hash=content_hash,
            dependencies=[],
            dependents=[],
            parameters=parameters,
            docstring=docstring
        )
    
    def _create_function_entity_generic(self, name: str, file_path: str, line_no: int, content: str) -> CodeEntity:
        """Create function entity for non-Python languages"""
        content_hash = self._hash_content(f"func_{name}_{line_no}")
        
        return CodeEntity(
            name=name,
            type='function',
            file_path=file_path,
            line_start=line_no,
            line_end=line_no,  # We'd need more complex parsing to find end line
            content_hash=content_hash,
            dependencies=[],
            dependents=[],
            parameters=[],  # Would need more complex parsing
            docstring=None
        )
    
    def _create_class_entity_python(self, node: ast.ClassDef, file_path: str, content: str) -> CodeEntity:
        """Create class entity for Python"""
        lines = content.split('\n')
        class_content = '\n'.join(lines[node.lineno-1:node.end_lineno])
        content_hash = self._hash_content(class_content)
        
        # Extract base classes
        dependencies = [base.id for base in node.bases if isinstance(base, ast.Name)]
        
        return CodeEntity(
            name=node.name,
            type='class',
            file_path=file_path,
            line_start=node.lineno,
            line_end=node.end_lineno,
            content_hash=content_hash,
            dependencies=dependencies,
            dependents=[]
        )
    
    def _create_class_entity_generic(self, name: str, file_path: str, line_no: int, content: str) -> CodeEntity:
        """Create class entity for non-Python languages"""
        content_hash = self._hash_content(f"class_{name}_{line_no}")
        
        return CodeEntity(
            name=name,
            type='class',
            file_path=file_path,
            line_start=line_no,
            line_end=line_no,  # Would need more complex parsing
            content_hash=content_hash,
            dependencies=[],
            dependents=[]
        )
    
    def _create_variable_entity(self, name: str, file_path: str, line_no: int, content: str) -> CodeEntity:
        """Create variable entity"""
        content_hash = self._hash_content(f"var_{name}_{line_no}")
        
        return CodeEntity(
            name=name,
            type='variable',
            file_path=file_path,
            line_start=line_no,
            line_end=line_no,
            content_hash=content_hash,
            dependencies=[],
            dependents=[]
        )
    
    def _analyze_python_dependencies(self, tree: ast.AST, file_path: str, entities: Dict[str, CodeEntity]):
        """Analyze function calls and variable usage for Python files"""
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    self.function_calls[file_path].add(func_name)
                    
                    # Find which function this call is inside
                    for entity_key, entity in entities.items():
                        if (entity.type == 'function' and 
                            entity.line_start <= node.lineno <= entity.line_end):
                            if f"func_{func_name}" in entities:
                                entity.dependencies.append(func_name)
                                entities[f"func_{func_name}"].dependents.append(entity.name)
            
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                var_name = node.id
                self.variable_usage[file_path].add(var_name)
    
    def _hash_content(self, content: str) -> str:
        """Create SHA-256 hash of content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()


class MerkleNode:
    """Node in the Merkle tree"""
    
    def __init__(self, name: str, hash_value: str = None, node_type: str = 'file'):
        self.name = name
        self.hash_value = hash_value
        self.node_type = node_type  # 'root', 'directory', 'file', 'entity'
        self.children = []
        self.metadata = {}
    
    def add_child(self, child):
        """Add a child node"""
        self.children.append(child)
    
    def calculate_hash(self):
        """Calculate hash based on children or own content"""
        if not self.children:
            # Leaf node - use existing hash
            return self.hash_value
        
        # Internal node - hash of all children's hashes
        child_hashes = []
        for child in self.children:
            child_hash = child.calculate_hash()
            child_hashes.append(child_hash)
        
        combined = ''.join(sorted(child_hashes))
        self.hash_value = hashlib.sha256(combined.encode('utf-8')).hexdigest()
        return self.hash_value


class MerkleTreeBuilder:
    """Builds Merkle tree from codebase analysis"""
    
    def __init__(self):
        self.root = None
        self.file_nodes = {}
        self.entity_nodes = {}
    
    def build_tree(self, codebase_path: str, all_entities: Dict[str, Dict[str, CodeEntity]]) -> MerkleNode:
        """Build complete Merkle tree from codebase"""
        self.root = MerkleNode("root", node_type='root')
        
        # Group entities by directory
        dir_structure = defaultdict(lambda: defaultdict(list))
        
        for file_path, entities in all_entities.items():
            rel_path = os.path.relpath(file_path, codebase_path)
            dir_name = os.path.dirname(rel_path)
            if not dir_name:
                dir_name = "."
            
            # Create file node
            file_node = MerkleNode(os.path.basename(file_path), node_type='file')
            
            # Add entity nodes to file
            for entity_key, entity in entities.items():
                entity_node = MerkleNode(
                    f"{entity.type}_{entity.name}",
                    entity.content_hash,
                    'entity'
                )
                entity_node.metadata = asdict(entity)
                file_node.add_child(entity_node)
                self.entity_nodes[f"{file_path}_{entity_key}"] = entity_node
            
            self.file_nodes[file_path] = file_node
            dir_structure[dir_name][file_path] = file_node
        
        # Build directory structure
        dir_nodes = {}
        for dir_name, files in dir_structure.items():
            if dir_name == ".":
                # Root directory files
                for file_path, file_node in files.items():
                    self.root.add_child(file_node)
            else:
                # Create directory node
                if dir_name not in dir_nodes:
                    dir_nodes[dir_name] = MerkleNode(dir_name, node_type='directory')
                    self.root.add_child(dir_nodes[dir_name])
                
                for file_path, file_node in files.items():
                    dir_nodes[dir_name].add_child(file_node)
        
        # Calculate all hashes
        self.root.calculate_hash()
        return self.root


class ChangeDetector:
    """Detects changes between Merkle trees"""
    
    def __init__(self):
        self.changes = []
    
    def compare_trees(self, old_tree: MerkleNode, new_tree: MerkleNode, path: str = "") -> List[Dict]:
        """Compare two Merkle trees and identify changes"""
        changes = []
        
        if old_tree.hash_value != new_tree.hash_value:
            if not old_tree.children and not new_tree.children:
                # Leaf node changed
                changes.append({
                    'type': 'modified',
                    'path': path,
                    'node_type': old_tree.node_type,
                    'old_hash': old_tree.hash_value,
                    'new_hash': new_tree.hash_value
                })
            else:
                # Directory or file changed - check children
                old_children = {child.name: child for child in old_tree.children}
                new_children = {child.name: child for child in new_tree.children}
                
                # Check for modifications and deletions
                for name, old_child in old_children.items():
                    if name in new_children:
                        child_changes = self.compare_trees(
                            old_child, new_children[name], f"{path}/{name}"
                        )
                        changes.extend(child_changes)
                    else:
                        changes.append({
                            'type': 'deleted',
                            'path': f"{path}/{name}",
                            'node_type': old_child.node_type
                        })
                
                # Check for additions
                for name, new_child in new_children.items():
                    if name not in old_children:
                        changes.append({
                            'type': 'added',
                            'path': f"{path}/{name}",
                            'node_type': new_child.node_type,
                            'hash': new_child.hash_value
                        })
        
        return changes


class MarkdownExporter:
    """Exports analysis results to markdown and DOT format"""
    
    def __init__(self):
        pass
    
    def export_dot(self, merkle_tree: MerkleNode, codebase_path: str, output_path: str):
        """Export Merkle tree to Graphviz DOT format"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("digraph CodebaseTree {\n")
            f.write("  node [shape=box];\n")
            f.write("  rankdir=BT;\n")  # Bottom-to-top direction
            
            # Helper function to write nodes and edges
            def write_node(node: MerkleNode, parent_id: str = None):
                node_id = f"node_{id(node)}"
                short_hash = node.hash_value[:8] if node.hash_value else "no-hash"
                label = f"{node.name}\\n[{short_hash}]"
                
                if node.node_type == "root":
                    label = f"Root\\n[{short_hash}]"
                    f.write(f'  {node_id} [label="{label}", shape=ellipse, style=filled, fillcolor=lightblue];\n')
                elif node.node_type == "directory":
                    f.write(f'  {node_id} [label="{label}", shape=folder, style=filled, fillcolor=lightyellow];\n')
                elif node.node_type == "file":
                    f.write(f'  {node_id} [label="{label}", style=filled, fillcolor=lightgreen];\n')
                else:  # entity
                    entity_type = node.metadata.get("type", "entity") if node.metadata else "entity"
                    f.write(f'  {node_id} [label="{label}\\n{entity_type}", style=filled, fillcolor=lightpink];\n')
                
                if parent_id:
                    f.write(f'  {node_id} -> {parent_id};\n')
                
                for child in node.children:
                    write_node(child, node_id)
            
            # Write the tree starting from root
            write_node(merkle_tree)
            f.write("}\n")
        
        print(f"DOT file exported to: {output_path}")
    
    def export_analysis(self, merkle_tree: MerkleNode, entities: Dict[str, Dict[str, CodeEntity]], 
                       codebase_path: str, output_path: str):
        """Export complete analysis to markdown"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # Header
            f.write("# Codebase Analysis Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Codebase:** `{codebase_path}`\n")
            f.write(f"**Root Hash:** `{merkle_tree.hash_value}`\n\n")
            
            # Overview section
            self._write_overview(f, merkle_tree, entities)
            
            # File structure
            self._write_file_structure(f, merkle_tree, entities, codebase_path)
            
            # Detailed analysis
            self._write_detailed_analysis(f, entities, codebase_path)
            
            # Dependency analysis
            self._write_dependency_analysis(f, entities)
            
            # Hash reference
            self._write_hash_reference(f, entities)
            
        print(f"Markdown analysis exported to: {output_path}")
    
    def _write_overview(self, f, merkle_tree: MerkleNode, entities: Dict):
        """Write overview section"""
        f.write("## 📊 Overview\n\n")
        
        total_files = len(entities)
        entity_counts = defaultdict(int)
        total_entities = 0
        
        for file_entities in entities.values():
            for entity in file_entities.values():
                entity_counts[entity.type] += 1
                total_entities += 1
        
        f.write(f"- **Total Files:** {total_files}\n")
        f.write(f"- **Total Code Entities:** {total_entities}\n")
        for entity_type, count in sorted(entity_counts.items()):
            f.write(f"  - {entity_type.title()}s: {count}\n")
        f.write("\n")
    
    def _write_file_structure(self, f, merkle_tree: MerkleNode, entities: Dict, codebase_path: str):
        """Write file structure section"""
        f.write("## 📁 File Structure\n\n")
        f.write("```\n")
        f.write(f"{os.path.basename(codebase_path)}/\n")
        
        # Group files by directory
        files_by_dir = defaultdict(list)
        for file_path in entities.keys():
            rel_path = os.path.relpath(file_path, codebase_path)
            dir_name = os.path.dirname(rel_path)
            if not dir_name:
                dir_name = "."
            files_by_dir[dir_name].append((rel_path, file_path))
        
        # Write structure
        for dir_name in sorted(files_by_dir.keys()):
            if dir_name != ".":
                f.write(f"├── {dir_name}/\n")
                for rel_path, full_path in sorted(files_by_dir[dir_name]):
                    file_name = os.path.basename(rel_path)
                    # Get file hash from first entity
                    file_hash = "no-hash"
                    if full_path in entities and entities[full_path]:
                        first_entity = next(iter(entities[full_path].values()))
                        file_hash = first_entity.content_hash[:8]
                    f.write(f"│   └── {file_name} [{file_hash}]\n")
        
        # Root directory files
        if "." in files_by_dir:
            for rel_path, full_path in sorted(files_by_dir["."]):
                file_name = os.path.basename(rel_path)
                file_hash = "no-hash"
                if full_path in entities and entities[full_path]:
                    first_entity = next(iter(entities[full_path].values()))
                    file_hash = first_entity.content_hash[:8]
                f.write(f"└── {file_name} [{file_hash}]\n")
        
        f.write("```\n\n")
    
    def _write_detailed_analysis(self, f, entities: Dict, codebase_path: str):
        """Write detailed file-by-file analysis"""
        f.write("## 🔍 Detailed File Analysis\n\n")
        
        for file_path in sorted(entities.keys()):
            rel_path = os.path.relpath(file_path, codebase_path)
            file_entities = entities[file_path]
            
            f.write(f"### 📄 `{rel_path}`\n\n")
            
            if not file_entities:
                f.write("*No code entities found*\n\n")
                continue
            
            # Group entities by type
            by_type = defaultdict(list)
            for entity in file_entities.values():
                by_type[entity.type].append(entity)
            
            # Write imports
            if 'import' in by_type:
                f.write("#### Imports\n")
                for entity in sorted(by_type['import'], key=lambda x: x.name):
                    f.write(f"- `{entity.name}` (line {entity.line_start}) `[{entity.content_hash[:8]}]`\n")
                f.write("\n")
            
            # Write classes
            if 'class' in by_type:
                f.write("#### Classes\n")
                for entity in sorted(by_type['class'], key=lambda x: x.name):
                    f.write(f"- **`{entity.name}`** (lines {entity.line_start}-{entity.line_end}) `[{entity.content_hash[:8]}]`\n")
                    if entity.dependencies:
                        f.write(f"  - *Inherits from:* {', '.join(entity.dependencies)}\n")
                    if entity.dependents:
                        f.write(f"  - *Used by:* {', '.join(entity.dependents)}\n")
                f.write("\n")
            
            # Write functions
            if 'function' in by_type:
                f.write("#### Functions\n")
                for entity in sorted(by_type['function'], key=lambda x: x.name):
                    params = f"({', '.join(entity.parameters)})" if entity.parameters else "()"
                    f.write(f"- **`{entity.name}{params}`** (lines {entity.line_start}-{entity.line_end}) `[{entity.content_hash[:8]}]`\n")
                    
                    if entity.docstring:
                        # First line of docstring only
                        first_line = entity.docstring.split('\n')[0].strip()
                        if first_line:
                            f.write(f"  - *{first_line}*\n")
                    
                    if entity.dependencies:
                        f.write(f"  - *Calls:* {', '.join(entity.dependencies)}\n")
                    if entity.dependents:
                        f.write(f"  - *Called by:* {', '.join(entity.dependents)}\n")
                f.write("\n")
            
            # Write variables
            if 'variable' in by_type:
                f.write("#### Variables\n")
                for entity in sorted(by_type['variable'], key=lambda x: x.name):
                    f.write(f"- `{entity.name}` (line {entity.line_start}) `[{entity.content_hash[:8]}]`\n")
                f.write("\n")
            
            f.write("---\n\n")
    
    def _write_dependency_analysis(self, f, entities: Dict):
        """Write dependency analysis section"""
        f.write("## 🔗 Dependency Analysis\n\n")
        
        # Function call graph
        function_deps = {}
        class_deps = {}
        
        for file_entities in entities.values():
            for entity in file_entities.values():
                if entity.type == 'function' and (entity.dependencies or entity.dependents):
                    function_deps[entity.name] = {
                        'calls': entity.dependencies,
                        'called_by': entity.dependents,
                        'file': os.path.basename(entity.file_path)
                    }
                elif entity.type == 'class' and (entity.dependencies or entity.dependents):
                    class_deps[entity.name] = {
                        'inherits': entity.dependencies,
                        'inherited_by': entity.dependents,
                        'file': os.path.basename(entity.file_path)
                    }
        
        # Write function dependencies
        if function_deps:
            f.write("### Function Dependencies\n\n")
            for func_name in sorted(function_deps.keys()):
                deps = function_deps[func_name]
                f.write(f"**`{func_name}`** *(in {deps['file']})*\n")
                if deps['calls']:
                    f.write(f"- Calls: {', '.join(deps['calls'])}\n")
                if deps['called_by']:
                    f.write(f"- Called by: {', '.join(deps['called_by'])}\n")
                f.write("\n")
        
        # Write class dependencies
        if class_deps:
            f.write("### Class Dependencies\n\n")
            for class_name in sorted(class_deps.keys()):
                deps = class_deps[class_name]
                f.write(f"**`{class_name}`** *(in {deps['file']})*\n")
                if deps['inherits']:
                    f.write(f"- Inherits from: {', '.join(deps['inherits'])}\n")
                if deps['inherited_by']:
                    f.write(f"- Inherited by: {', '.join(deps['inherited_by'])}\n")
                f.write("\n")
    
    def _write_hash_reference(self, f, entities: Dict):
        """Write hash reference for change tracking"""
        f.write("## 🔐 Hash Reference\n\n")
        f.write("*Use these hashes to track changes between analyses*\n\n")
        
        f.write("| Entity | Type | File | Hash |\n")
        f.write("|--------|------|------|------|\n")
        
        all_entities = []
        for file_path, file_entities in entities.items():
            for entity in file_entities.values():
                all_entities.append((entity.name, entity.type, os.path.basename(file_path), entity.content_hash[:12]))
        
        for name, entity_type, file_name, hash_short in sorted(all_entities):
            f.write(f"| `{name}` | {entity_type} | {file_name} | `{hash_short}` |\n")
        
        f.write("\n")
        f.write("## 📝 Usage Notes\n\n")
        f.write("- Each entity has a unique hash based on its content\n")
        f.write("- When code changes, the hash changes, enabling precise change detection\n")
        f.write("- Dependencies show how functions and classes connect to each other\n")
        f.write("- Use this report to understand code structure and track modifications\n")
        f.write("- Upload this markdown file to AI assistants for code analysis and questions\n\n")


class CodebaseAnalyzer:
    """Main analyzer class that orchestrates the entire process"""
    
    def __init__(self, codebase_path: str):
        self.codebase_path = Path(codebase_path)
        self.parser = CodeParser()
        self.tree_builder = MerkleTreeBuilder()
        self.change_detector = ChangeDetector()
        self.markdown_exporter = MarkdownExporter()
        self.supported_extensions = {'.py', '.java', '.kt', '.swift'}  # Multi-language support
    
    def analyze(self) -> Tuple[MerkleNode, Dict[str, Dict[str, CodeEntity]]]:
        """Analyze the entire codebase"""
        print(f"Analyzing codebase at: {self.codebase_path}")
        
        all_entities = {}
        file_count = 0
        
        # Walk through all files
        for file_path in self._get_code_files():
            print(f"Parsing: {file_path}")
            entities = self.parser.parse_file(str(file_path))
            if entities:
                all_entities[str(file_path)] = entities
                file_count += 1
        
        print(f"Parsed {file_count} files")
        print(f"Found {sum(len(entities) for entities in all_entities.values())} code entities")
        
        # Build Merkle tree
        print("Building Merkle tree...")
        merkle_tree = self.tree_builder.build_tree(str(self.codebase_path), all_entities)
        
        return merkle_tree, all_entities
    
    def _get_code_files(self):
        """Get all code files in the codebase"""
        for file_path in self.codebase_path.rglob('*'):
            if (file_path.is_file() and 
                file_path.suffix in self.supported_extensions and
                not self._should_ignore(file_path)):
                yield file_path
    
    def _should_ignore(self, file_path: Path) -> bool:
        """Check if file should be ignored"""
        # Ignore any directory or file that starts with a dot
        for part in file_path.parts:
            if part.startswith('.'):
                return True
        
        # Additional ignore patterns
        ignore_patterns = {
            '__pycache__', 'venv', 'env', 'virtualenv',
            'node_modules', 'build', 'dist', 'target',
            'out', 'bin', 'obj', 'libs', 'dependencies',
            'Pods', 'DerivedData', 'xcuserdata',
            'gradle', 'gradlew', 'gradlew.bat'
        }
        
        # Check if any part of the path matches ignore patterns
        for part in file_path.parts:
            if part in ignore_patterns:
                return True
        
        # Ignore specific file patterns
        ignore_file_patterns = {
            file_path.name.startswith('.'),  # Any file starting with dot
            file_path.suffix in {'.pyc', '.pyo', '.class', '.jar', '.war', '.dex'},
            file_path.name in {'gradlew', 'gradlew.bat', 'Podfile.lock', 'Package.resolved'}
        }
        
        return any(ignore_file_patterns)
    
    def save_analysis(self, merkle_tree: MerkleNode, entities: Dict, output_path: str, format_type: str = 'json'):
        """Save analysis results in specified format"""
        if format_type.lower() == 'markdown' or format_type.lower() == 'md':
            self.markdown_exporter.export_analysis(
                merkle_tree, entities, str(self.codebase_path), output_path
            )
            # Generate DOT file alongside markdown
            dot_output = output_path.rsplit('.', 1)[0] + '.dot'
            self.markdown_exporter.export_dot(merkle_tree, str(self.codebase_path), dot_output)
        else:
            # JSON format (original)
            def serialize_node(node: MerkleNode):
                return {
                    'name': node.name,
                    'hash_value': node.hash_value,
                    'node_type': node.node_type,
                    'metadata': node.metadata,
                    'children': [serialize_node(child) for child in node.children]
                }
            
            # Convert entities to serializable format
            serializable_entities = {}
            for file_path, file_entities in entities.items():
                serializable_entities[file_path] = {
                    key: asdict(entity) for key, entity in file_entities.items()
                }
            
            analysis_data = {
                'merkle_tree': serialize_node(merkle_tree),
                'entities': serializable_entities,
                'root_hash': merkle_tree.hash_value,
                'codebase_path': str(self.codebase_path),
                'generated_at': datetime.now().isoformat()
            }
            
            with open(output_path, 'w') as f:
                json.dump(analysis_data, f, indent=2)
            
            print(f"JSON analysis saved to: {output_path}")
    
    def print_summary(self, merkle_tree: MerkleNode, entities: Dict):
        """Print analysis summary"""
        print("\n" + "="*60)
        print("CODEBASE ANALYSIS SUMMARY")
        print("="*60)
        print(f"Root Hash: {merkle_tree.hash_value}")
        print(f"Total Files: {len(entities)}")
        
        entity_counts = defaultdict(int)
        dependency_count = 0
        
        for file_entities in entities.values():
            for entity in file_entities.values():
                entity_counts[entity.type] += 1
                dependency_count += len(entity.dependencies)
        
        print(f"Code Entities:")
        for entity_type, count in entity_counts.items():
            print(f"  - {entity_type.capitalize()}s: {count}")
        
        print(f"Total Dependencies: {dependency_count}")
        
        print("\nFile Structure:")
        self._print_tree(merkle_tree, 0)
    
    def _print_tree(self, node: MerkleNode, depth: int):
        """Print tree structure"""
        if depth > 3:  # Limit depth for readability
            return
            
        indent = "  " * depth
        hash_short = node.hash_value[:8] if node.hash_value else "no-hash"
        print(f"{indent}{node.name} ({node.node_type}) [{hash_short}]")
        
        for child in node.children[:5]:  # Limit children shown
            self._print_tree(child, depth + 1)
        
        if len(node.children) > 5:
            print(f"{indent}  ... and {len(node.children) - 5} more")


def main():
    parser = argparse.ArgumentParser(description='Analyze codebase and build Merkle tree')
    parser.add_argument('path', help='Path to codebase directory')
    parser.add_argument('--output', '-o', help='Output file for analysis results', 
                       default='codebase_analysis')
    parser.add_argument('--format', '-f', choices=['json', 'markdown', 'md'], 
                       default='markdown', help='Output format (default: markdown)')
    parser.add_argument('--compare', '-c', help='Compare with previous analysis file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: Path {args.path} does not exist")
        sys.exit(1)
    
    # Determine output file extension
    if args.format.lower() in ['markdown', 'md']:
        if not args.output.endswith('.md'):
            output_file = f"{args.output}.md"
        else:
            output_file = args.output
    else:
        if not args.output.endswith('.json'):
            output_file = f"{args.output}.json"
        else:
            output_file = args.output
    
    # Analyze codebase
    analyzer = CodebaseAnalyzer(args.path)
    merkle_tree, entities = analyzer.analyze()
    
    # Print summary
    analyzer.print_summary(merkle_tree, entities)
    
    # Save results
    analyzer.save_analysis(merkle_tree, entities, output_file, args.format)
    
    # Compare with previous analysis if requested
    if args.compare:
        if os.path.exists(args.compare):
            print(f"\nComparing with previous analysis: {args.compare}")
            print("Comparison feature coming soon...")
        else:
            print(f"Warning: Comparison file {args.compare} does not exist")
    
    print(f"\n✅ Analysis complete!")
    print(f"📊 Root hash: {merkle_tree.hash_value}")
    print(f"📄 Report saved: {output_file}")
    print(f"\n💡 You can now upload '{output_file}' to Claude or other AI assistants for code analysis!")


if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
import os
import re
from collections import Counter
from datetime import datetime
import string

class FileStatsAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("File Statistics Analyzer - Comprehensive Edition")
        self.root.geometry("900x700")
        
        # Browse button
        self.browse_btn = tk.Button(root, text="Browse File", command=self.browse_file, 
                                    font=("Arial", 12), bg="#4CAF50", fg="white", 
                                    padx=20, pady=10)
        self.browse_btn.pack(pady=20)
        
        # File path label
        self.file_label = tk.Label(root, text="No file selected", font=("Arial", 10), 
                                   fg="gray")
        self.file_label.pack()
        
        # Results text area with larger size
        self.results_text = scrolledtext.ScrolledText(root, width=100, height=35, 
                                                      font=("Courier", 9), 
                                                      wrap=tk.WORD)
        self.results_text.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
    def browse_file(self):
        filepath = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("All files", "*.*"), 
                      ("Python files", "*.py"), 
                      ("HTML files", "*.html"),
                      ("CSS files", "*.css"),
                      ("JavaScript files", "*.js"),
                      ("JSON files", "*.json"),
                      ("XML files", "*.xml"),
                      ("Text files", "*.txt")]
        )
        
        if filepath:
            self.file_label.config(text=f"File: {os.path.basename(filepath)}")
            self.analyze_file(filepath)
    
    def browse_file(self):
        filepath = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("All files", "*.*"), 
                      ("Python files", "*.py"), 
                      ("HTML files", "*.html"),
                      ("CSS files", "*.css"),
                      ("JavaScript files", "*.js"),
                      ("JSON files", "*.json"),
                      ("XML files", "*.xml"),
                      ("Text files", "*.txt")]
        )
        
        if filepath:
            self.file_label.config(text=f"File: {os.path.basename(filepath)}")
            self.analyze_file(filepath)
    
    def analyze_file(self, filepath):
        try:
            # Try different encodings
            content = None
            encoding_used = None
            for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'ascii']:
                try:
                    with open(filepath, 'r', encoding=encoding) as f:
                        content = f.read()
                    encoding_used = encoding
                    break
                except:
                    continue
            
            if content is None:
                self.results_text.delete(1.0, tk.END)
                self.results_text.insert(tk.END, "Error: Could not decode file with common encodings")
                return
            
            # Get file metadata
            file_stats = os.stat(filepath)
            
            stats = self.calculate_stats(content, filepath, encoding_used, file_stats)
            self.display_stats(stats)
            
        except Exception as e:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Error reading file: {str(e)}")
    
    def detect_line_ending(self, content):
        crlf = content.count('\r\n')
        lf = content.count('\n') - crlf
        cr = content.count('\r') - crlf
        
        if crlf > lf and crlf > cr:
            return "CRLF (Windows)"
        elif lf > crlf and lf > cr:
            return "LF (Unix/Mac)"
        elif cr > 0:
            return "CR (Old Mac)"
        return "Mixed/Unknown"
    
    def calculate_readability(self, content):
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        words = content.split()
        
        if not words or not sentences:
            return None
        
        # Simple Flesch Reading Ease approximation
        syllables = sum(self.count_syllables(word) for word in words)
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = syllables / len(words)
        
        flesch_score = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word
        
        return {
            'flesch_score': flesch_score,
            'sentences': len(sentences),
            'avg_sentence_length': avg_sentence_length,
            'avg_syllables_per_word': avg_syllables_per_word
        }
    
    def count_syllables(self, word):
        word = word.lower()
        vowels = "aeiouy"
        count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                count += 1
            prev_was_vowel = is_vowel
        
        if word.endswith('e'):
            count -= 1
        if count == 0:
            count = 1
            
        return count
    
    def calculate_stats(self, content, filepath, encoding, file_stats):
        lines = content.split('\n')
        ext = os.path.splitext(filepath)[1].lower()
        
        stats = {
            'filename': os.path.basename(filepath),
            'filepath': filepath,
            'file_size': len(content.encode('utf-8')),
            'encoding': encoding,
            'has_bom': content.startswith('\ufeff'),
            'line_ending': self.detect_line_ending(content),
            
            # Time metadata
            'created': datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            'modified': datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'accessed': datetime.fromtimestamp(file_stats.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
            
            # Basic counts
            'total_chars': len(content),
            'total_lines': len(lines),
            'non_empty_lines': len([l for l in lines if l.strip()]),
            'empty_lines': len([l for l in lines if not l.strip()]),
            'total_words': len(content.split()),
            'unique_words': len(set(content.lower().split())),
            
            # Character types
            'spaces': content.count(' '),
            'tabs': content.count('\t'),
            'newlines': content.count('\n'),
            'alphabetic': sum(c.isalpha() for c in content),
            'numeric': sum(c.isdigit() for c in content),
            'uppercase': sum(c.isupper() for c in content),
            'lowercase': sum(c.islower() for c in content),
            'special_chars': sum(not c.isalnum() and not c.isspace() for c in content),
            'non_ascii': sum(ord(c) > 127 for c in content),
            
            # Punctuation
            'commas': content.count(','),
            'periods': content.count('.'),
            'semicolons': content.count(';'),
            'colons': content.count(':'),
            'exclamations': content.count('!'),
            'questions': content.count('?'),
            
            # Brackets and quotes
            'parentheses_open': content.count('('),
            'parentheses_close': content.count(')'),
            'braces_open': content.count('{'),
            'braces_close': content.count('}'),
            'brackets_open': content.count('['),
            'brackets_close': content.count(']'),
            'angle_brackets_open': content.count('<'),
            'angle_brackets_close': content.count('>'),
            'single_quotes': content.count("'"),
            'double_quotes': content.count('"'),
            'backticks': content.count('`'),
        }
        
        # Lexical diversity
        if stats['total_words'] > 0:
            stats['lexical_diversity'] = stats['unique_words'] / stats['total_words']
        else:
            stats['lexical_diversity'] = 0
        
        # Word statistics
        words = content.split()
        if words:
            word_lengths = [len(w) for w in words]
            stats['avg_word_length'] = sum(word_lengths) / len(word_lengths)
            stats['max_word_length'] = max(word_lengths)
            stats['min_word_length'] = min(word_lengths)
            
            # Most common words (excluding very short ones)
            word_freq = Counter(w.lower() for w in words if len(w) > 3)
            stats['top_words'] = word_freq.most_common(10)
        else:
            stats['avg_word_length'] = 0
            stats['max_word_length'] = 0
            stats['min_word_length'] = 0
            stats['top_words'] = []
        
        # Indentation analysis
        indents = []
        stats['trailing_whitespace_lines'] = 0
        for line in lines:
            if line and line != line.rstrip():
                stats['trailing_whitespace_lines'] += 1
            if line and line[0] in [' ', '\t']:
                leading_spaces = len(line) - len(line.lstrip(' '))
                leading_tabs = len(line) - len(line.lstrip('\t'))
                indents.append(max(leading_spaces, leading_tabs))
        
        stats['indented_lines'] = len(indents)
        stats['avg_indentation'] = sum(indents) / len(indents) if indents else 0
        stats['max_indentation'] = max(indents) if indents else 0
        
        # Line length analysis
        line_lengths = [len(line) for line in lines]
        stats['avg_line_length'] = sum(line_lengths) / len(line_lengths) if line_lengths else 0
        stats['max_line_length'] = max(line_lengths) if line_lengths else 0
        stats['min_line_length'] = min(line_lengths) if line_lengths else 0
        stats['lines_over_79'] = len([l for l in lines if len(l) > 79])
        stats['lines_over_99'] = len([l for l in lines if len(l) > 99])
        
        # Nesting depth
        max_nesting = 0
        current_nesting = 0
        for char in content:
            if char in '({[':
                current_nesting += 1
                max_nesting = max(max_nesting, current_nesting)
            elif char in ')}]':
                current_nesting = max(0, current_nesting - 1)
        stats['max_nesting_depth'] = max_nesting
        
        # Character frequency (top 15)
        char_freq = Counter(content)
        stats['char_frequency'] = char_freq.most_common(15)
        
        # Readability metrics
        readability = self.calculate_readability(content)
        if readability:
            stats.update(readability)
        
        # Python specific
        if ext == '.py':
            stats['python_comments'] = len([l for l in lines if l.strip().startswith('#')])
            stats['python_imports'] = len([l for l in lines if 'import' in l])
            stats['python_functions'] = len(re.findall(r'\bdef\s+\w+\s*\(', content))
            stats['python_classes'] = len(re.findall(r'\bclass\s+\w+', content))
            stats['python_decorators'] = len(re.findall(r'@\w+', content))
            stats['python_f_strings'] = len(re.findall(r'f["\']', content))
            stats['python_list_comp'] = len(re.findall(r'\[.*for.*in.*\]', content))
            stats['python_try_except'] = len(re.findall(r'\btry:', content))
            stats['python_docstrings'] = len(re.findall(r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'', content))
            stats['python_type_hints'] = len(re.findall(r':\s*\w+\s*[,\)]', content))
            stats['python_todos'] = len(re.findall(r'#\s*(TODO|FIXME|NOTE|HACK|XXX)', content, re.IGNORECASE))
            
            # String literals
            single_strings = re.findall(r"'[^']*'", content)
            double_strings = re.findall(r'"[^"]*"', content)
            all_strings = single_strings + double_strings
            stats['string_literals'] = len(all_strings)
            if all_strings:
                stats['avg_string_length'] = sum(len(s) - 2 for s in all_strings) / len(all_strings)
            else:
                stats['avg_string_length'] = 0
        
        # HTML specific
        elif ext in ['.html', '.htm']:
            stats['html_tags'] = len(re.findall(r'<[^>]+>', content))
            stats['html_comments'] = len(re.findall(r'<!--.*?-->', content, re.DOTALL))
            stats['html_div_tags'] = len(re.findall(r'<div\b', content, re.IGNORECASE))
            stats['html_script_tags'] = len(re.findall(r'<script\b', content, re.IGNORECASE))
            stats['html_style_tags'] = len(re.findall(r'<style\b', content, re.IGNORECASE))
            stats['html_img_tags'] = len(re.findall(r'<img\b', content, re.IGNORECASE))
            stats['html_a_tags'] = len(re.findall(r'<a\b', content, re.IGNORECASE))
            
            # Attribute count
            attributes = re.findall(r'\w+\s*=\s*["\'][^"\']*["\']', content)
            stats['html_attributes'] = len(attributes)
        
        # CSS specific
        elif ext == '.css':
            stats['css_selectors'] = len(re.findall(r'[.#\w\s>+~\[\]:]+\s*{', content))
            stats['css_properties'] = len(re.findall(r'[\w-]+\s*:', content))
            stats['css_comments'] = len(re.findall(r'/\*.*?\*/', content, re.DOTALL))
            stats['css_media_queries'] = len(re.findall(r'@media', content))
            stats['css_classes'] = len(set(re.findall(r'\.[\w-]+', content)))
            stats['css_ids'] = len(set(re.findall(r'#[\w-]+', content)))
        
        # JavaScript specific
        elif ext == '.js':
            stats['js_functions'] = len(re.findall(r'\bfunction\s+\w+\s*\(', content))
            stats['js_arrow_functions'] = len(re.findall(r'=>', content))
            stats['js_var_declarations'] = len(re.findall(r'\bvar\s+\w+', content))
            stats['js_let_declarations'] = len(re.findall(r'\blet\s+\w+', content))
            stats['js_const_declarations'] = len(re.findall(r'\bconst\s+\w+', content))
            stats['js_comments_single'] = len(re.findall(r'//.*', content))
            stats['js_comments_multi'] = len(re.findall(r'/\*.*?\*/', content, re.DOTALL))
            stats['js_template_literals'] = len(re.findall(r'`[^`]*`', content))
        
        # JSON specific
        elif ext == '.json':
            try:
                import json
                json_data = json.loads(content)
                stats['json_valid'] = True
                stats['json_depth'] = self.get_json_depth(json_data)
                stats['json_keys'] = self.count_json_keys(json_data)
            except:
                stats['json_valid'] = False
        
        # XML specific
        elif ext == '.xml':
            stats['xml_tags'] = len(re.findall(r'<[^/>][^>]*>', content))
            stats['xml_self_closing'] = len(re.findall(r'<[^>]+/>', content))
            stats['xml_comments'] = len(re.findall(r'<!--.*?-->', content, re.DOTALL))
        
        return stats
    
    def get_json_depth(self, obj, depth=0):
        if isinstance(obj, dict):
            if not obj:
                return depth
            return max(self.get_json_depth(v, depth + 1) for v in obj.values())
        elif isinstance(obj, list):
            if not obj:
                return depth
            return max(self.get_json_depth(item, depth + 1) for item in obj)
        return depth
    
    def count_json_keys(self, obj):
        count = 0
        if isinstance(obj, dict):
            count += len(obj)
            for v in obj.values():
                count += self.count_json_keys(v)
        elif isinstance(obj, list):
            for item in obj:
                count += self.count_json_keys(item)
        return count
    
    def display_stats(self, stats):
        self.results_text.delete(1.0, tk.END)
        
        output = f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    COMPREHENSIVE FILE STATISTICS REPORT                   ║
╚═══════════════════════════════════════════════════════════════════════════╝

📁 FILE INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
File Name:             {stats['filename']}
File Size:             {stats['file_size']:,} bytes ({stats['file_size']/1024:.2f} KB)
Encoding:              {stats['encoding']}
BOM Present:           {'Yes' if stats['has_bom'] else 'No'}
Line Endings:          {stats['line_ending']}

📅 TIME METADATA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Created:               {stats['created']}
Modified:              {stats['modified']}
Last Accessed:         {stats['accessed']}

📊 CHARACTER STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Characters:      {stats['total_chars']:,}
Alphabetic:            {stats['alphabetic']:,}
Numeric:               {stats['numeric']:,}
Uppercase:             {stats['uppercase']:,}
Lowercase:             {stats['lowercase']:,}
Special Characters:    {stats['special_chars']:,}
Non-ASCII Characters:  {stats['non_ascii']:,}
Spaces:                {stats['spaces']:,}
Tabs:                  {stats['tabs']:,}
Newlines:              {stats['newlines']:,}

📝 LINE STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Lines:           {stats['total_lines']:,}
Non-Empty Lines:       {stats['non_empty_lines']:,}
Empty Lines:           {stats['empty_lines']:,}
Average Line Length:   {stats['avg_line_length']:.2f} chars
Maximum Line Length:   {stats['max_line_length']:,} chars
Minimum Line Length:   {stats['min_line_length']:,} chars
Lines Over 79 Chars:   {stats['lines_over_79']:,}
Lines Over 99 Chars:   {stats['lines_over_99']:,}
Trailing Whitespace:   {stats['trailing_whitespace_lines']:,} lines

🔤 WORD STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Words:           {stats['total_words']:,}
Unique Words:          {stats['unique_words']:,}
Lexical Diversity:     {stats['lexical_diversity']:.4f}
Average Word Length:   {stats['avg_word_length']:.2f} chars
Maximum Word Length:   {stats['max_word_length']:,} chars
Minimum Word Length:   {stats['min_word_length']:,} chars

⬆️ INDENTATION STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Indented Lines:        {stats['indented_lines']:,}
Average Indentation:   {stats['avg_indentation']:.2f} spaces
Maximum Indentation:   {stats['max_indentation']:,} spaces

🔣 PUNCTUATION STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Commas (,):            {stats['commas']:,}
Periods (.):           {stats['periods']:,}
Semicolons (;):        {stats['semicolons']:,}
Colons (:):            {stats['colons']:,}
Exclamations (!):      {stats['exclamations']:,}
Questions (?):         {stats['questions']:,}

🔐 BRACKETS & QUOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Parentheses ( ):       {stats['parentheses_open']:,} open, {stats['parentheses_close']:,} close
Braces {{ }}:            {stats['braces_open']:,} open, {stats['braces_close']:,} close
Brackets [ ]:          {stats['brackets_open']:,} open, {stats['brackets_close']:,} close
Angle Brackets < >:    {stats['angle_brackets_open']:,} open, {stats['angle_brackets_close']:,} close
Single Quotes ('):     {stats['single_quotes']:,}
Double Quotes ("):     {stats['double_quotes']:,}
Backticks (`):         {stats['backticks']:,}

🏗️ CODE STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Max Nesting Depth:     {stats['max_nesting_depth']}
"""
        
        # Readability metrics
        if 'flesch_score' in stats:
            output += f"""
📖 READABILITY METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Flesch Reading Ease:   {stats['flesch_score']:.2f}
Sentences:             {stats['sentences']:,}
Avg Sentence Length:   {stats['avg_sentence_length']:.2f} words
Avg Syllables/Word:    {stats['avg_syllables_per_word']:.2f}
"""
        
        # Top words
        if stats['top_words']:
            output += f"""
🔝 TOP 10 MOST FREQUENT WORDS (>3 chars)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            for word, count in stats['top_words']:
                output += f"{word:>20} : {count:,} times\n"
        
        # Character frequency
        output += f"""
🔤 TOP 15 MOST FREQUENT CHARACTERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        for char, count in stats['char_frequency']:
            char_display = repr(char) if char in [' ', '\n', '\t', '\r'] else char
            output += f"{char_display:>8} : {count:,} times\n"
        
        # Python specific stats
        if 'python_comments' in stats:
            output += f"""
🐍 PYTHON SPECIFIC STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Comment Lines (#):     {stats['python_comments']:,}
Import Statements:     {stats['python_imports']:,}
Function Definitions:  {stats['python_functions']:,}
Class Definitions:     {stats['python_classes']:,}
Decorators (@):        {stats['python_decorators']:,}
F-strings:             {stats['python_f_strings']:,}
List Comprehensions:   {stats['python_list_comp']:,}
Try-Except Blocks:     {stats['python_try_except']:,}
Docstrings:            {stats['python_docstrings']:,}
Type Hints:            {stats['python_type_hints']:,}
TODO/FIXME Comments:   {stats['python_todos']:,}
String Literals:       {stats['string_literals']:,}
Avg String Length:     {stats['avg_string_length']:.2f} chars
"""
        
        # HTML specific stats
        elif 'html_tags' in stats:
            output += f"""
🌐 HTML SPECIFIC STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total HTML Tags:       {stats['html_tags']:,}
HTML Comments:         {stats['html_comments']:,}
Div Tags:              {stats['html_div_tags']:,}
Script Tags:           {stats['html_script_tags']:,}
Style Tags:            {stats['html_style_tags']:,}
Image Tags:            {stats['html_img_tags']:,}
Anchor Tags:           {stats['html_a_tags']:,}
Total Attributes:      {stats['html_attributes']:,}
"""
        
        # CSS specific stats
        elif 'css_selectors' in stats:
            output += f"""
🎨 CSS SPECIFIC STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CSS Selectors:         {stats['css_selectors']:,}
CSS Properties:        {stats['css_properties']:,}
CSS Comments:          {stats['css_comments']:,}
Media Queries:         {stats['css_media_queries']:,}
Unique Classes:        {stats['css_classes']:,}
Unique IDs:            {stats['css_ids']:,}
"""
        
        # JavaScript specific stats
        elif 'js_functions' in stats:
            output += f"""
⚡ JAVASCRIPT SPECIFIC STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Function Declarations: {stats['js_functions']:,}
Arrow Functions:       {stats['js_arrow_functions']:,}
Var Declarations:      {stats['js_var_declarations']:,}
Let Declarations:      {stats['js_let_declarations']:,}
Const Declarations:    {stats['js_const_declarations']:,}
Single-line Comments:  {stats['js_comments_single']:,}
Multi-line Comments:   {stats['js_comments_multi']:,}
Template Literals:     {stats['js_template_literals']:,}
"""
        
        # JSON specific stats
        elif 'json_valid' in stats:
            if stats['json_valid']:
                output += f"""
📋 JSON SPECIFIC STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Valid JSON:            Yes
JSON Nesting Depth:    {stats['json_depth']}
Total JSON Keys:       {stats['json_keys']:,}
"""
            else:
                output += f"""
📋 JSON SPECIFIC STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Valid JSON:            No (Parse Error)
"""
        
        # XML specific stats
        elif 'xml_tags' in stats:
            output += f"""
📄 XML SPECIFIC STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
XML Tags:              {stats['xml_tags']:,}
Self-closing Tags:     {stats['xml_self_closing']:,}
XML Comments:          {stats['xml_comments']:,}
"""
        
        output += "\n" + "═" * 80 + "\n"
        output += "Analysis Complete!\n"
        
        self.results_text.insert(tk.END, output)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileStatsAnalyzer(root)
    root.mainloop()
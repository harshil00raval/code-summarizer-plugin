import os
import re
# from enum import Enum

# class Language(Enum):
#     JAVA = 'java'
#     PYTHON = 'python'
#     GROOVY = 'groovy'

class Language:
    PYTHON = "python"
    JAVA = "java"
    GROOVY = "groovy"

class CleaningConfig:
    def __init__(self,
                 remove_empty_methods=True,
                 remove_getters_setters=False,
                 remove_logging=True,
                 remove_empty_catches=True,
                 remove_unused_variables=True,
                 summarize_annotations=True,
                 keep_method_signatures=True):
        self.remove_empty_methods = remove_empty_methods
        self.remove_getters_setters = remove_getters_setters
        self.remove_logging = remove_logging
        self.remove_empty_catches = remove_empty_catches
        self.remove_unused_variables = remove_unused_variables
        self.summarize_annotations = summarize_annotations
        self.keep_method_signatures = keep_method_signatures

class AdvancedCodeSummarizer:
    def __init__(self):
        self.import_patterns = {
            Language.JAVA: r'^import\s+.*?;$',
            Language.PYTHON: r'^(?:from|import)\s+.*$',
            Language.GROOVY: r'^import\s+.*?$'
        }

        self.comment_patterns = {
            Language.JAVA: [r'//.*$', r'/\*[\s\S]*?\*/'],
            Language.PYTHON: [r'#.*$', r'"""[\s\S]*?"""', r"'''[\s\S]*?'''"],
            Language.GROOVY: [r'//.*$', r'/\*[\s\S]*?\*/']
        }

        # Language-specific patterns
        self.patterns = {
            'getter_setter': {
                Language.JAVA: r'(?:public|private)\s+\w+\s+(?:get|set)\w+\s*\([^)]*\)\s*\{[^}]*\}',
                Language.PYTHON: r'@property\s*\ndef\s+\w+\s*\([^)]*\)[^:]*:.*?(?=\S)|@\w+\.setter.*?(?=\S)',
                Language.GROOVY: r'(?:def|public)\s+(?:get|set)\w+\s*\([^)]*\)\s*\{[^}]*\}'
            },
            'logging': {
                Language.JAVA: r'(?:log|logger|LOGGER)\.(?:debug|info|warn|error)\([^;]*\);',
                Language.PYTHON: r'(?:logging|logger)\.(?:debug|info|warning|error)\([^)]*\)',
                Language.GROOVY: r'(?:log|logger)\.(?:debug|info|warn|error)\([^)]*\)'
            },
            'empty_catch': {
                Language.JAVA: r'catch\s*\([^)]*\)\s*\{\s*\}',
                Language.PYTHON: r'except[^:]*:\s*pass',
                Language.GROOVY: r'catch\s*\([^)]*\)\s*\{\s*\}'
            },
            'empty_method': {
                Language.JAVA: r'(?:public|private|protected)\s+\w+\s+\w+\s*\([^)]*\)\s*\{\s*\}',
                Language.PYTHON: r'def\s+\w+\s*\([^)]*\)\s*:\s*(?:pass\s*)?$',
                Language.GROOVY: r'def\s+\w+\s*\([^)]*\)\s*\{\s*\}'
            }
        }

    def clean_code(self, content, language, config):

        """
        Advanced code cleaning with configurable options.
        """
        cleaned = content

        print(config)
        # Remove comments first
        for pattern in self.comment_patterns[language]:
            cleaned = re.sub(pattern, '', cleaned, flags=re.MULTILINE)

        # if config.remove_getters_setters:
        cleaned = re.sub(self.patterns['getter_setter'][language], '', cleaned)

        # if config.remove_logging:
        cleaned = re.sub(self.patterns['logging'][language], '', cleaned)

        # if config.remove_empty_catches:
        cleaned = re.sub(self.patterns['empty_catch'][language], '', cleaned)

        # if config.remove_empty_methods:
        cleaned = re.sub(self.patterns['empty_method'][language], '', cleaned)

        # Language-specific cleaning
        if language == Language.JAVA:
            cleaned = self._clean_java(cleaned, config)
            cleaned = self._clean_java_logs_and_comments(cleaned)
            cleaned = self._remove_spring_api_annotations(cleaned)
        elif language == Language.PYTHON:
            cleaned = self._clean_python(cleaned, config)

        return self._normalize_whitespace(cleaned)

    def _clean_java(self, content, config):
        # Preserve annotations on a single line
        content = re.sub(r'(@\w+\s*(?:\([^)]*\))?\s*\n\s*)+', lambda m: m.group().replace('\n', ' '), content)

        # Remove unused private fields (both initialized and uninitialized)
        content = re.sub(r'private\s+\w+\s+\w+\s*;?', '', content)

        return content

    def _clean_java_logs_and_comments(self,content) :
        """
        Removes print statements, logging statements, and comments (including TODOs) from Java code.

        :param content: The input Java code as a string.
        :return: Cleaned Java code with logs and comments removed.
        """

        # Remove logging statements (e.g., log.info(...), log.debug(...), log.error(...), log.warn(...))
        content = re.sub(r'\blog\.\w+\(.*?\);\s*', '', content)

        # Remove System.out.print and System.out.println statements
        content = re.sub(r'System\.out\.(print|println)\(.*?\);\s*', '', content)

        # Remove single-line comments (// ...)
        content = re.sub(r'//.*', '', content)

        # Remove multi-line comments (/* ... */)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

        # Remove TODO comments (case insensitive)
        content = re.sub(r'//\s*TODO:?.*', '', content, flags=re.IGNORECASE)

        return content
    def _remove_spring_api_annotations(self, content):
        """
        Removes Spring Boot API documentation annotations like @Operation, @ApiResponses, etc.
        Handles multiline annotations, nested structures, and string concatenations.

        Args:
            content: The Java code content as a string
            config: Configuration options

        Returns:
            The cleaned Java code with API annotations removed
        """
        # List of Spring API documentation annotations to remove
        spring_api_annotations = [
            r'@Operation',
            r'@ApiResponses?',
            r'@ApiResponse',
            r'@Parameter',
            r'@Parameters',
            r'@Schema',
            r'@Tag',
            r'@ApiParam',
            r'@ApiOperation',
            r'@ApiModel',
            r'@ApiModelProperty',
            r'@ApiImplicitParams?',
            r'@ApiImplicitParam'
            r'@JsonProperty'
            r'@JsonIgnore'
        ]

        # Process the content line by line
        lines = content.split('\n')
        result_lines = []
        i = 0

        while i < len(lines):
            line = lines[i]
            skip_line = False

            # Check if line contains any of the target annotations
            for annotation in spring_api_annotations:
                if re.search(annotation + r'\b', line):
                    skip_line = True

                    # Handle multiline annotation with parentheses
                    if '(' in line and ')' not in line:
                        # Count opening and closing parentheses
                        open_parens = line.count('(')
                        close_parens = line.count(')')
                        balance = open_parens - close_parens

                        # Continue counting until balance is restored
                        j = i + 1
                        while j < len(lines) and balance > 0:
                            next_line = lines[j]
                            open_parens = next_line.count('(')
                            close_parens = next_line.count(')')
                            balance += open_parens - close_parens

                            # Check for string concatenation with +
                            if balance == 0 and next_line.strip().endswith('+'):
                                balance = 1  # Force continuation

                            j += 1

                        # Skip all lines that were part of this annotation
                        i = j - 1
                    break

            # Add line if it shouldn't be skipped
            if not skip_line:
                # Remove @RequestBody annotation but keep the parameter
                if '@RequestBody' in line:
                    line = re.sub(r'@RequestBody\s+', '', line)
                result_lines.append(line)

            i += 1

        # Join the lines back together
        result = '\n'.join(result_lines)

        # Clean up any artifacts left over (commas, empty lines, etc.)
        result = re.sub(r',\s*,', '', result)  # Remove consecutive commas
        result = re.sub(r'\{\s*,', '{', result)  # Remove comma after opening brace
        result = re.sub(r',\s*\}', '}', result)  # Remove comma before closing brace
        result = re.sub(r'\n\s*\n\s*\n', '\n\n', result)  # Remove excessive blank lines
        result = re.sub(r'\s*\{\s*\}\s*\n', '', result)  # Remove empty braces

        return result


    def _clean_python(self, content, config):
        """Python-specific cleaning"""
        # if config.remove_unused_variables:
            # Remove unused imports
        content = re.sub(r'from \w+ import \w+(?:, \w+)*\n(?!.*\w+)', '', content)

        # Simplify type hints if not used
        content = re.sub(r':\s*[A-Z]\w+(?:\[.*?\])?(?=\s*=)', ':', content)

        return content


    def _normalize_whitespace(self, content):
        """Normalize whitespace while preserving structure"""
        # Remove multiple empty lines
        content = re.sub(r'\n\s*\n', '\n\n', content)
        # Remove trailing whitespace
        content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)
        return content.strip()

    def extract_method_signatures(self, content, language):
        """Extract method signatures for documentation"""
        patterns = {
            Language.JAVA: r'(?:public|private|protected)\s+\w+\s+\w+\s*\([^)]*\)',
            Language.PYTHON: r'def\s+\w+\s*\([^)]*\)',
            Language.GROOVY: r'def\s+\w+\s*\([^)]*\)'
        }

        return re.findall(patterns[language], content)

    def process_file(self, content, language, config) :
        """
        Process a single file with advanced cleaning options.
        """
        # Extract imports first
        imports = []
        for line in content.split('\n'):
            if re.match(self.import_patterns[language], line.strip()):
                imports.append(line.strip())

        # Clean the code
        cleaned_content = self.clean_code(content, language, config)

        # Extract method signatures if configured
        signatures = []
        # if config.keep_method_signatures:
        signatures = self.extract_method_signatures(content, language)

        return {
            'imports': imports,
            'cleaned_content': cleaned_content,
            'method_signatures': signatures,
            'token_estimate': self.estimate_tokens(cleaned_content)
        }

    def estimate_tokens(self, text) :
        """Improved token estimation"""
        # Count words
        word_count = len(text.split())
        # Count symbols and punctuation
        symbol_count = len(re.findall(r'[^\w\s]', text))
        # Rough estimation based on GPT tokenization patterns
        return word_count + symbol_count + (len(text) // 6)
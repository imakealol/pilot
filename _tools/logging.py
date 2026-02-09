#!/usr/bin/env python3
"""
Pilot Project - Unified Logging Utility

Comprehensive logging with consistent formatting across all scripts.
Logs to console with colors and optionally to timestamped files.

Usage:
    from logging import Logger

    # Basic usage
    log = Logger('my_script')
    log.info('Starting process')
    log.success('Completed successfully')
    log.warning('Something to note')
    log.error('Something went wrong')

    # With file logging
    log = Logger('my_script', log_to_file=True)

    # With context
    log = Logger('my_script', context={'chapter': 38, 'agent': 'continuity'})

    # Structured data
    log.data('Results', {'found': 5, 'fixed': 3})

    # Progress tracking
    log.progress(3, 10, 'Processing chapters')

    # Section headers
    log.section('Phase 1: Analysis')
    log.divider()
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from contextlib import contextmanager
import traceback


# =============================================================================
# CONFIGURATION
# =============================================================================

LOG_DIR = Path('/workspaces/pilot/_tools/logs')

class Level(Enum):
    """Log levels with priority ordering."""
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    CRITICAL = 50


# ANSI color codes for terminal output
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright variants
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'


# Level to color mapping
LEVEL_COLORS = {
    Level.DEBUG: Colors.DIM,
    Level.INFO: Colors.CYAN,
    Level.SUCCESS: Colors.GREEN,
    Level.WARNING: Colors.YELLOW,
    Level.ERROR: Colors.RED,
    Level.CRITICAL: Colors.BRIGHT_RED + Colors.BOLD,
}

# Level symbols for visual scanning
LEVEL_SYMBOLS = {
    Level.DEBUG: '·',
    Level.INFO: '→',
    Level.SUCCESS: '✓',
    Level.WARNING: '⚠',
    Level.ERROR: '✗',
    Level.CRITICAL: '‼',
}


# =============================================================================
# LOG ENTRY
# =============================================================================

@dataclass
class LogEntry:
    """Single log entry with all metadata."""
    timestamp: str
    level: str
    source: str
    message: str
    context: Dict[str, Any] = field(default_factory=dict)
    data: Optional[Any] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        d = {
            'timestamp': self.timestamp,
            'level': self.level,
            'source': self.source,
            'message': self.message,
        }
        if self.context:
            d['context'] = self.context
        if self.data is not None:
            d['data'] = self.data
        if self.error:
            d['error'] = self.error
        return d

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), default=str)


# =============================================================================
# LOGGER CLASS
# =============================================================================

class Logger:
    """
    Unified logging with consistent formatting.

    Features:
    - Colored console output with level indicators
    - Optional file logging with JSON format
    - Context tracking (add metadata to all logs)
    - Structured data logging
    - Progress indicators
    - Section headers and dividers
    - Indentation for nested operations
    - Timer context manager
    """

    def __init__(
        self,
        source: str,
        level: Level = Level.INFO,
        log_to_file: bool = False,
        log_file: Optional[Path] = None,
        use_colors: bool = True,
        context: Optional[Dict[str, Any]] = None,
        quiet: bool = False,
    ):
        """
        Initialize logger.

        Args:
            source: Name of the script/module using this logger
            level: Minimum log level to output
            log_to_file: Whether to also log to file
            log_file: Custom log file path (default: logs/{source}_{date}.log)
            use_colors: Whether to use ANSI colors in console output
            context: Default context to include with all log entries
            quiet: Suppress console output (file logging still works)
        """
        self.source = source
        self.level = level
        self.use_colors = use_colors and sys.stdout.isatty()
        self.context = context or {}
        self.quiet = quiet
        self._indent = 0
        self._entries: list[LogEntry] = []

        # File logging setup
        self.log_to_file = log_to_file
        self.log_file = log_file
        if log_to_file and not log_file:
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            date_str = datetime.now().strftime('%Y%m%d')
            self.log_file = LOG_DIR / f'{source}_{date_str}.log'

    # -------------------------------------------------------------------------
    # Core Logging Methods
    # -------------------------------------------------------------------------

    def _log(
        self,
        level: Level,
        message: str,
        data: Optional[Any] = None,
        error: Optional[Exception] = None,
        extra_context: Optional[Dict] = None,
    ):
        """Internal logging method."""
        if level.value < self.level.value:
            return

        timestamp = datetime.now().isoformat(timespec='milliseconds')

        # Merge context
        ctx = {**self.context}
        if extra_context:
            ctx.update(extra_context)

        # Create entry
        entry = LogEntry(
            timestamp=timestamp,
            level=level.name,
            source=self.source,
            message=message,
            context=ctx,
            data=data,
            error=traceback.format_exc() if error else None,
        )
        self._entries.append(entry)

        # Console output
        if not self.quiet:
            self._print_console(level, message, data)

        # File output
        if self.log_to_file and self.log_file:
            self._write_file(entry)

    def _print_console(self, level: Level, message: str, data: Optional[Any] = None):
        """Print formatted output to console."""
        indent = '  ' * self._indent
        symbol = LEVEL_SYMBOLS[level]

        if self.use_colors:
            color = LEVEL_COLORS[level]
            reset = Colors.RESET
            dim = Colors.DIM

            # Timestamp
            ts = datetime.now().strftime('%H:%M:%S')

            # Format: [HH:MM:SS] ✓ Message
            line = f"{dim}[{ts}]{reset} {color}{symbol}{reset} {indent}{message}"
        else:
            ts = datetime.now().strftime('%H:%M:%S')
            line = f"[{ts}] {symbol} {indent}{message}"

        print(line)

        # Print data if present
        if data is not None:
            self._print_data(data)

    def _print_data(self, data: Any, indent_level: int = 1):
        """Print structured data with indentation."""
        indent = '  ' * (self._indent + indent_level)
        dim = Colors.DIM if self.use_colors else ''
        reset = Colors.RESET if self.use_colors else ''

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    print(f"{dim}{indent}{key}:{reset}")
                    self._print_data(value, indent_level + 1)
                else:
                    print(f"{dim}{indent}{key}: {value}{reset}")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    self._print_data(item, indent_level)
                else:
                    print(f"{dim}{indent}- {item}{reset}")
        else:
            print(f"{dim}{indent}{data}{reset}")

    def _write_file(self, entry: LogEntry):
        """Write entry to log file."""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(entry.to_json() + '\n')

    # -------------------------------------------------------------------------
    # Public Logging Methods
    # -------------------------------------------------------------------------

    def debug(self, message: str, data: Optional[Any] = None, **context):
        """Log debug message."""
        self._log(Level.DEBUG, message, data, extra_context=context or None)

    def info(self, message: str, data: Optional[Any] = None, **context):
        """Log info message."""
        self._log(Level.INFO, message, data, extra_context=context or None)

    def success(self, message: str, data: Optional[Any] = None, **context):
        """Log success message."""
        self._log(Level.SUCCESS, message, data, extra_context=context or None)

    def warning(self, message: str, data: Optional[Any] = None, **context):
        """Log warning message."""
        self._log(Level.WARNING, message, data, extra_context=context or None)

    def warn(self, message: str, data: Optional[Any] = None, **context):
        """Alias for warning."""
        self.warning(message, data, **context)

    def error(self, message: str, error: Optional[Exception] = None, data: Optional[Any] = None, **context):
        """Log error message."""
        self._log(Level.ERROR, message, data, error=error, extra_context=context or None)

    def critical(self, message: str, error: Optional[Exception] = None, data: Optional[Any] = None, **context):
        """Log critical message."""
        self._log(Level.CRITICAL, message, data, error=error, extra_context=context or None)

    def data(self, label: str, data: Any):
        """Log structured data with a label."""
        self._log(Level.INFO, label, data)

    # -------------------------------------------------------------------------
    # Formatting Helpers
    # -------------------------------------------------------------------------

    def section(self, title: str):
        """Print a section header."""
        if not self.quiet:
            width = 60
            if self.use_colors:
                print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * width}{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.BLUE}{title.center(width)}{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.BLUE}{'=' * width}{Colors.RESET}\n")
            else:
                print(f"\n{'=' * width}")
                print(f"{title.center(width)}")
                print(f"{'=' * width}\n")

    def subsection(self, title: str):
        """Print a subsection header."""
        if not self.quiet:
            if self.use_colors:
                print(f"\n{Colors.BOLD}{Colors.CYAN}--- {title} ---{Colors.RESET}\n")
            else:
                print(f"\n--- {title} ---\n")

    def divider(self, char: str = '-'):
        """Print a horizontal divider."""
        if not self.quiet:
            width = 60
            if self.use_colors:
                print(f"{Colors.DIM}{char * width}{Colors.RESET}")
            else:
                print(char * width)

    def blank(self):
        """Print a blank line."""
        if not self.quiet:
            print()

    def progress(self, current: int, total: int, label: str = ''):
        """Display progress indicator."""
        if self.quiet:
            return

        pct = (current / total * 100) if total > 0 else 0
        bar_width = 30
        filled = int(bar_width * current / total) if total > 0 else 0
        bar = '█' * filled + '░' * (bar_width - filled)

        if self.use_colors:
            color = Colors.CYAN if pct < 100 else Colors.GREEN
            print(f"\r{color}[{bar}] {current}/{total} ({pct:.0f}%){Colors.RESET} {label}", end='')
        else:
            print(f"\r[{bar}] {current}/{total} ({pct:.0f}%) {label}", end='')

        if current >= total:
            print()  # Newline when complete

    # -------------------------------------------------------------------------
    # Context Managers
    # -------------------------------------------------------------------------

    @contextmanager
    def indent(self):
        """Context manager for indented logging."""
        self._indent += 1
        try:
            yield
        finally:
            self._indent -= 1

    @contextmanager
    def task(self, name: str):
        """
        Context manager for tracking a task.

        Logs start/end and handles errors.

        Usage:
            with log.task('Processing chapter'):
                # ... do work ...
        """
        self.info(f"Starting: {name}")
        self._indent += 1
        start = datetime.now()

        try:
            yield
            elapsed = (datetime.now() - start).total_seconds()
            self._indent -= 1
            self.success(f"Completed: {name} ({elapsed:.2f}s)")
        except Exception as e:
            self._indent -= 1
            self.error(f"Failed: {name}", error=e)
            raise

    @contextmanager
    def timer(self, label: str):
        """
        Context manager for timing operations.

        Usage:
            with log.timer('API call'):
                response = api.call()
        """
        start = datetime.now()
        try:
            yield
        finally:
            elapsed = (datetime.now() - start).total_seconds()
            self.debug(f"{label}: {elapsed:.3f}s")

    # -------------------------------------------------------------------------
    # Context Management
    # -------------------------------------------------------------------------

    def set_context(self, **kwargs):
        """Add to the default context for all logs."""
        self.context.update(kwargs)

    def clear_context(self):
        """Clear the default context."""
        self.context = {}

    @contextmanager
    def with_context(self, **kwargs):
        """Temporarily add context for a block of code."""
        old_context = self.context.copy()
        self.context.update(kwargs)
        try:
            yield
        finally:
            self.context = old_context

    # -------------------------------------------------------------------------
    # Summary and Export
    # -------------------------------------------------------------------------

    def get_entries(self, level: Optional[Level] = None) -> list[LogEntry]:
        """Get logged entries, optionally filtered by level."""
        if level is None:
            return self._entries
        return [e for e in self._entries if Level[e.level].value >= level.value]

    def get_errors(self) -> list[LogEntry]:
        """Get all error and critical entries."""
        return self.get_entries(Level.ERROR)

    def summary(self) -> Dict[str, int]:
        """Get count of entries by level."""
        counts = {level.name: 0 for level in Level}
        for entry in self._entries:
            counts[entry.level] += 1
        return counts

    def print_summary(self):
        """Print a summary of all logged entries."""
        counts = self.summary()
        total = len(self._entries)

        self.divider()
        self.info(f"Log Summary: {total} total entries")
        with self.indent():
            for level in Level:
                count = counts[level.name]
                if count > 0:
                    self._log(level, f"{level.name}: {count}", data=None)
        self.divider()


# =============================================================================
# MODULE-LEVEL CONVENIENCE FUNCTIONS
# =============================================================================

# Default logger instance
_default_logger: Optional[Logger] = None


def get_logger(source: str = 'pilot', **kwargs) -> Logger:
    """Get or create a logger instance."""
    global _default_logger
    if _default_logger is None or _default_logger.source != source:
        _default_logger = Logger(source, **kwargs)
    return _default_logger


def configure(source: str = 'pilot', **kwargs):
    """Configure the default logger."""
    global _default_logger
    _default_logger = Logger(source, **kwargs)


# Quick access functions using default logger
def debug(message: str, **kwargs):
    get_logger().debug(message, **kwargs)

def info(message: str, **kwargs):
    get_logger().info(message, **kwargs)

def success(message: str, **kwargs):
    get_logger().success(message, **kwargs)

def warning(message: str, **kwargs):
    get_logger().warning(message, **kwargs)

def error(message: str, **kwargs):
    get_logger().error(message, **kwargs)

def critical(message: str, **kwargs):
    get_logger().critical(message, **kwargs)


# =============================================================================
# CLI FOR TESTING
# =============================================================================

def main():
    """Demo the logging functionality."""
    log = Logger('demo', level=Level.DEBUG, log_to_file=True)

    log.section('Logging Utility Demo')

    # Basic levels
    log.debug('This is a debug message')
    log.info('This is an info message')
    log.success('This is a success message')
    log.warning('This is a warning message')
    log.error('This is an error message')

    log.blank()

    # Structured data
    log.subsection('Structured Data')
    log.data('Analysis Results', {
        'chapters_processed': 7,
        'issues_found': 12,
        'issues_fixed': 10,
        'breakdown': {
            'timeline': 3,
            'continuity': 5,
            'voice': 4
        }
    })

    log.blank()

    # Progress
    log.subsection('Progress Indicator')
    for i in range(1, 11):
        log.progress(i, 10, f'Processing item {i}')

    log.blank()

    # Task tracking
    log.subsection('Task Tracking')
    try:
        with log.task('Processing chapters'):
            log.info('Loading chapter 38')
            log.info('Analyzing content')
            log.success('Found 3 issues')
    except Exception:
        pass

    log.blank()

    # Context
    log.subsection('Context Tracking')
    log.set_context(agent='continuity_editor', chapter=38)
    log.info('Analyzing with context')
    log.info('Still has context')
    log.clear_context()
    log.info('Context cleared')

    # Summary
    log.print_summary()

    print(f"\nLog file: {log.log_file}")


if __name__ == '__main__':
    main()

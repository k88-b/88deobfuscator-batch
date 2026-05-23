# -*- coding: utf-8 -*-

import sys
import os
from core.config import AppConfig
from core.patterns import Patterns
from core.file_manager import FileManager
from core.code_executor import CodeExecutor
from core.pattern_matcher import PatternMatcher
from core.exceptions import DeobfuscationError
from ui import CliOutput
from utils import DefineObfuscation
from decoders.registry import DECODER_REGISTRY


class App:
    def __init__(self):
        self.config = AppConfig()
        self.patterns = Patterns()
        self.output = CliOutput()
        self.file_manager = FileManager(self.output, self.config)
        self.code_executor = CodeExecutor(self.output)
        self.pattern_matcher = PatternMatcher(self.output, self.patterns)

    def _list_methods(self) -> None:
        print("Available obfuscation methods:")
        print("  auto (default) - automatic detection")
        for key in sorted(DECODER_REGISTRY.keys()):
            print(f"  {key}")
        sys.exit(0)

    def _auto_detect_method(self, file_name: str) -> str:
        print("Auto‑detecting obfuscation type...")
        definer = DefineObfuscation(
            file_name=file_name,
            cli_output=self.output,
            file_manager=self.file_manager,
        )
        method_key = definer.detect()
        if method_key is None:
            raise DeobfuscationError(
                "Could not detect obfuscation type. "
                "Please specify it manually with --method."
            )
        print(f"Detected obfuscation: {method_key}")
        return method_key

    def run(self, args) -> None:
        if args.list:
            self._list_methods()
            return

        input_file = args.input_file

        if args.output:
            output_file = args.output
        else:
            base = os.path.basename(input_file)
            output_file = os.path.join(
                os.path.dirname(input_file),
                f"{self.config.DECODED_FILE_PREFIX}{base}"
            )

        if args.method:
            method_key = args.method
            if method_key == "auto":
                method_key = self._auto_detect_method(input_file)
            elif method_key not in DECODER_REGISTRY:
                self.output.print_error(
                    f"Unknown method '{method_key}'. Use --list to see available methods."
                )
                sys.exit(1)
            else:
                print(f"Using manually selected method: {method_key}")
        else:
            method_key = self._auto_detect_method(input_file)

        decoder_class = DECODER_REGISTRY[method_key]

        decoder = decoder_class(
            file_name=input_file,
            new_file_name=output_file,
            method_key=method_key,
            cli_output=self.output,
            file_manager=self.file_manager,
            code_executor=self.code_executor,
            pattern_matcher=self.pattern_matcher,
            config=self.config,
            patterns=self.patterns,
        )

        try:
            decoder.decode()
        except DeobfuscationError as e:
            self.output.print_error(str(e))
            sys.exit(1)
        except Exception as e:
            self.output.print_error(f"Unexpected error: {e}")
            sys.exit(1)

        print(f"Successfully deobfuscated! Check {output_file}")

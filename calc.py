import sys
from antlr4 import *
from EvalVisitor import EvalVisitor
import importlib

def load_parser_and_lexer(use_alt):
    if use_alt:
        lexer_mod = 'labeldExpr_altLexer'
        parser_mod = 'labeldExpr_altParser'
        lexer_cls = 'labeldExpr_altLexer'
        parser_cls = 'labeldExpr_altParser'
    else:
        lexer_mod = 'labeldExprLexer'
        parser_mod = 'labeldExprParser'
        lexer_cls = 'labeldExprLexer'
        parser_cls = 'labeldExprParser'

    try:
        lexer_module = importlib.import_module(lexer_mod)
        parser_module = importlib.import_module(parser_mod)
    except ModuleNotFoundError as e:
        print(f"ERROR: módulo faltante: {e}. Asegúrate de haber generado los .py con ANTLR y que están en este directorio.")
        sys.exit(1)

    Lexer = getattr(lexer_module, lexer_cls)
    Parser = getattr(parser_module, parser_cls)
    return Lexer, Parser

def main(argv):
    use_alt = False
    filename = None
    for arg in argv[1:]:
        if arg == "--alt":
            use_alt = True
        else:
            filename = arg

    Lexer, Parser = load_parser_and_lexer(use_alt)

    if filename:
        data = FileStream(filename, encoding="utf-8")
    else:
        data = InputStream(sys.stdin.read())

    lexer = Lexer(data)
    tokens = CommonTokenStream(lexer)
    parser = Parser(tokens)
    tree = parser.prog()

    evaluator = EvalVisitor()
    evaluator.visit(tree)

if __name__ == "__main__":
    main(sys.argv)


grammar labeldExpr;

prog: stat* EOF ;

stat
  : expr NEWLINE             #PrintExpr
  | ID '=' expr NEWLINE      #Assign
  | NEWLINE                  #Blank
  ;

expr
  : expr POW expr            #Pow
  | expr op=(MUL | DIV) expr #MulDiv
  | expr op=(ADD | SUB) expr #AddSub
  | expr FACT                #Fact
  | SUB expr                 #UnaryMinus
  | ID '(' expr ')'          #Function
  | INT                      #Int
  | DOUBLE                   #Double
  | ID                       #Id
  | '(' expr ')'             #Parens
  ;

ADD : '+' ;
SUB : '-' ;
MUL : '*' ;
DIV : '/' ;
POW : '^' ;
FACT: '!' ;

ID  : [a-zA-Z_] [a-zA-Z_0-9]* ;
DOUBLE : [0-9]+ '.' [0-9]+ ;
INT : [0-9]+ ;

NEWLINE : ('\r'? '\n')+ ;
WS : [ \t]+ -> skip ;


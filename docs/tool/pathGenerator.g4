grammar PathGenerator;

pathgenerator: '路径函数生成' BGNL pathstat+
/* pathgenerator
var initcode = `
var prestr=''
var cpre = function(add){
    if(add==null)add=4;
    if(add>0)prestr+=Array(add+1).join(' ');
    if(add<0)prestr=prestr.slice(0,-add);
}
var clen = function(){
    return prestr.length;
}
var output=[]
var push=function(str){output.push(str)}
var pushln=function(str){output.push(prestr,str,'\\n')}
pushln('def path(painter):')
cpre()
pushln('length=0')
`

var endcode=`
pushln('return length')
cpre(-4)
setoutput(output.join(''))
`

var code = '(function(setoutput){\n'+initcode+pathstat_0+endcode+'})(setoutput);\n';
return code;
*/;

pathstat: go|leftright|repeat|void;

go: '直行' Number
/* go
default : [100000]
var code = 'pushln("length+=painter.Straight('+Number_0+')");\n';
return code;
*/;

leftright: LeftRight_List '半径' Number Number '度'
/*  leftright
default : [null,50000,90]
LeftRight_List_0=LeftRight_List_0=='left'?'-':''
var code = 'pushln("length+=painter.Turning('+LeftRight_List_0+Number_0+','+Number_1+')");\n';
return code;
*/;

repeat: '重复' Int '次' BGNL pathstat+
/*  repeat
default : [5]
colour : this.controlColor
var code = 'pushln("for _index"+clen()+" in range('+Int_0+'):");\ncpre();\n;'+pathstat_0+'cpre(-4);\n';
return code;
*/;

void: Nothing
/*  void
colour : this.controlColor
var code = 'pushln("pass");\n';
return code;
*/;

statExprSplit : '=== statement ^ === expression v ===' ;

LeftRight_List : '左转'|'右转'/* LeftRight_List ['left','right'] */;

Int :   [0-9]+ ;

Number
    :   '-'? Int '.' Int EXP?   // 1.35, 1.35E-9, 0.3, -4.5
    |   '-'? Int EXP            // 1e10 -3e4
    |   '-'? Int                // -3, 45
    ;
fragment EXP : [Ee] [+\-]? Int ; // \- since - means "range" inside [...]

BGNL
    :   ('BGNLaergayergfuybgv'+)?
    ;

MeaningfulSplit : '=== meaningful ^ ===' ;

Nothing : ('vaueisbrvyuebrg'+)?;

/* Function_0
//this.evisitor.recieveOrder='ORDER_NONE';
this.evisitor.valueColor=330;
this.evisitor.statementColor=70;
this.evisitor.entryColor=250;

this.evisitor.idstring_eColor=310;
this.evisitor.subColor=190;
this.evisitor.printColor=70;
this.evisitor.controlColor=130;
this.evisitor.eventColor=220;
this.evisitor.soundColor=20;
*/
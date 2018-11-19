%%
%{
% data demo
TBD_projectname_xy={};
xx_=[-250000,-250000,250000,250000];
yy_=[-250000,-30000,-30000,-250000];
TBD_projectname_xy{end+1}={xx_,yy_};
xx_=[-250000,-250000,250000,250000];
yy_=[-25000,-15000,-15000,-25000];
TBD_projectname_xy{end+1}={xx_,yy_};
xx_=[-250000,-250000,250000,250000];
yy_=[-10000,10000,10000,-10000];
TBD_projectname_xy{end+1}={xx_,yy_};
xx_=[-250000,-250000,250000,250000];
yy_=[15000,25000,25000,15000];
TBD_projectname_xy{end+1}={xx_,yy_};
xx_=[-250000,-250000,250000,250000];
yy_=[30000,250000,250000,30000];
TBD_projectname_xy{end+1}={xx_,yy_};
TBD_projectname_ports=[[-250000,-20000], [250000,-20000]];
TBD_projectname_porttype=[0, 0];
TBD_projectname_parametertype='Y';
TBD_projectname_speed=0;
TBD_projectname_extra='{"json": "nothing, null will lead a bug in jsonlab-matlab"}';
TBD_projectname_boxsize=[500000, 500000];
TBD_projectname_sweep=[4, 8, 2];
project_name_='TBD_projectname';
%}
%=====^ data ^=====v simulate v=====
% json=struct('loads',@(str)subsref(loadjson(['["",' str ']']),struct('type','{}','subs',{{2}})),'dumps',@(obj)savejson('',obj));
json=struct('loads',@(str)jsondecode(str),'dumps',@(obj)jsonencode(obj));
TBD_projectname_extra=json.loads(TBD_projectname_extra);
Project=SonnetProject();
Project.saveAs([project_name_,'.son']);
% length unit
Project.changeLengthUnit('UM');
Project.changeFrequencyUnit('GHZ');
% box size and cell size
unitratio_=0.001;
TBD_projectname_boxsize=TBD_projectname_boxsize*unitratio_;
Project.changeBoxSize(TBD_projectname_boxsize(1),TBD_projectname_boxsize(2));
if TBD_projectname_speed==0
Project.changeCellSizeUsingNumberOfCells(1,1);
else
    Project.changeCellSizeUsingNumberOfCells(2,2);
end
% Set the dielectric layer thicknesses
Project.changeDielectricLayerThickness(1,50);
Project.changeDielectricLayerThickness(2,50);
% % Delete the default second layer so we can replace it with a new alumina one
% Project.deleteLayer(2);
% % Add the alumina layer to the Project.
% Project.addDielectricLayer('Alumina',20,9.8,1,1.0e-4,0,0);
%
offset_=TBD_projectname_boxsize/2;
TBD_projectname_polygon={};
for ii = TBD_projectname_xy
    xx_=ii{1}{1}*unitratio_+offset_(1);
    yy_=ii{1}{2}*unitratio_+offset_(2);
    TBD_projectname_polygon{end+1}=Project.addMetalPolygonEasy(0,xx_,yy_);
    Project.changePolygonType(TBD_projectname_polygon{end},'Lossless');
end
%
TBD_projectname_ports=TBD_projectname_ports*unitratio_;
portnum_=0;
for ii = 2:2:size(TBD_projectname_ports,2)
    portnum_=portnum_+1;
    if TBD_projectname_porttype(portnum_)==1
        addPortCocalibratedAtLocation(Project.GeometryBlock,TBD_projectname_ports(ii-1)+offset_(1),TBD_projectname_ports(ii)+offset_(2));
    else
        Project.addPortAtLocation(TBD_projectname_ports(ii-1)+offset_(1),TBD_projectname_ports(ii)+offset_(2));
end
end
%
% Project.addSimpleFrequencySweep(TBD_projectname_sweep(1),TBD_projectname_sweep(2),TBD_projectname_sweep(3));
Project.addAbsFrequencySweep(TBD_projectname_sweep(1),TBD_projectname_sweep(2));
Project.ControlBlock.TargetAbs=TBD_projectname_sweep(3);
Project.ControlBlock.Speed=TBD_projectname_speed;
% Add an output file and then resimulate
% Project.addTouchstoneOutput;
Project.addFileOutput('TS','D','Y',['$BASENAME.s' num2str(portnum_) 'p'],'IC','Y',TBD_projectname_parametertype,'RI','R',50)
% Project.openInSonnet();
Project.saveAs([project_name_,'.son']);
%===================================
%%
fid=fopen([project_name_,'.son'],'r');
str=fread(fid);
fclose(fid);
str=char(str');
%
startDir = pwd;
targetDir=fileparts(mfilename('fullpath'));
if isempty(targetDir)
    targetDir=pwd;
end
cd(targetDir);
pymod = py.importlib.import_module('fixFormat');  
py.importlib.reload(pymod);    
cd(startDir);
str=char(pymod.fixOneLayerFile(str));
%
fid=fopen([project_name_,'.son'],'w');
fprintf(fid,'%s',str);
fclose(fid);
%===================================
%%
Project=SonnetProject([project_name_,'.son']);
TBD_projectname_Project=Project;
Project.simulate('-c');
%===================================
%%
% Read Touchstone Output File for S11 and S21
snpfilename_=[project_name_,'.s',num2str(portnum_),'p'];
S11 = TouchstoneParser(snpfilename_,1,1);
S21 = TouchstoneParser(snpfilename_,2,1);
% Convert the S11 and S21 data to dB
S11dB = 20*log10(abs(S11(:,2)));
S21dB = 20*log10(abs(S21(:,2)));
% Plot S11 and S21 data in dB
F = S11(:,1);
plot(F,S11dB,F,S21dB);
title('dB(S_2_1) and dB(S_1_1) vs Freq.');
xlabel('F [GHz]');
ylabel('dB(S)');
legend('dB(S_1_1)','dB(S_2_1)','Location','Best')
grid on
%
% Project.viewResponseData();
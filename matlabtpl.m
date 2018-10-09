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
TBD_projectname_extra='null';
TBD_projectname_boxsize=[500000, 500000];
TBD_projectname_sweep=[4, 8, 2];
project_name_='TBD_projectname';
%}
%=====^ data ^=====v simulate v=====
TBD_projectname_extra=jsondecode(TBD_projectname_extra);
Project=SonnetProject();
Project.saveAs([project_name_,'.son']);
% length unit
Project.changeLengthUnit('UM');
Project.changeFrequencyUnit('GHZ');
% box size and cell size
unitratio_=0.001;
TBD_projectname_boxsize=TBD_projectname_boxsize*unitratio_;
Project.changeBoxSize(TBD_projectname_boxsize(1),TBD_projectname_boxsize(2));
Project.changeCellSizeUsingNumberOfCells(1,1);
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
        myaddPortCocalibrated(Project.GeometryBlock,TBD_projectname_ports(ii-1)+offset_(1),TBD_projectname_ports(ii)+offset_(2));
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
try
    lines=split(str,sprintf('\n'));
    clines=cell(1,size(lines,1));
    for ii = 1:size(clines,2)
        clines{ii}=char(lines(ii));
    end
catch
    clines=strsplit(str,sprintf('\n'));
end
for ii = 1:size(clines,2)
    if strcmp(clines{ii}(1:3) , 'BOX')
        boxindex=ii;
        break
    end
end
clines=cat(2,...
    {clines{1}},...
    {'VER 14.52'},...
    clines{3:boxindex-1},...
    {'MET "Al" 1 NOR INF 0 0.1 '},...
    {clines{boxindex}},...
    {...
        '      2000 1 1 0 0 0 0 "Air"',...
        '      500 9.3 1 3e-006 0 0 0 "Sapphire" A 11.5 1 3e-006 0 0 ',...
        'TECHLAY METAL Al <UNSPECIFIED> 10 0 ',...
        '0 0 0 N 0 1 1 100 100 0 0 0 Y',...
        'END',...
        'END',...
        'LORGN 0 1000 U '...
    },...
    clines{boxindex+3:end}...
);
for ii = boxindex:size(clines,2)
    if size(clines{ii},2)>=3 && strcmp(clines{ii}(1:3) , 'NUM')
        numindex=ii;
        break
    end
end
insertindexs=[];
insertindexs(end+1)=numindex;
for ii = numindex:size(clines,2)
    if size(clines{ii},2)>=7 && strcmp(clines{ii}(1:7) , 'END GEO')
        break
    end
    if size(clines{ii},2)>=3 && strcmp(clines{ii}(1:3) , 'END')
        insertindexs(end+1)=ii;
    end
end
insertindexs=insertindexs(1:end-1);
templines={};
lastindex=0;
for ii = insertindexs
    templines=cat(2,templines,clines(lastindex+1:ii+1),{'TLAYNAM Al INH'});
    lastindex=ii+1;
end
clines=cat(2,templines,clines(lastindex+1:end));
%
fid=fopen([project_name_,'.son'],'w');
for ii = 1:size(clines,2)
    fprintf(fid,'%s\n',char(clines{ii}));
end
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
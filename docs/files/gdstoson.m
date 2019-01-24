function gdstoson
% Make a Sonnet Project
Project=SonnetProject();

gdsname = 'cg.gds';
cellsize = 2;
freqstart = 4;
freqstop = 8;
freqabs = 300;

Project.changeLengthUnit('UM');
Project.changeFrequencyUnit('GHZ');
% Set the dielectric layer
Project.replaceDielectricLayer(1,'Vacuum',2000,1,1,0,0,0)
Project.replaceDielectricLayer(2,'Sapphire',430,9.3,1,1e-6,0,0,11.5,1,1e-6,0,0)

glib = read_gds_library(gdsname);
mybox = bbox(glib(1));
Project.changeBoxSize(mybox(3)-mybox(1),mybox(4)-mybox(2));
Project.changeCellSizeUsingNumberOfCells(cellsize,cellsize);

boundaryXL{1} = [mybox(2) mybox(4)];
boundaryXR{1} = [mybox(2) mybox(4)];
boundaryYB{1} = [mybox(1) mybox(3)];
boundaryYT{1} = [mybox(1) mybox(3)];

% Add a metal polygon
for i = 1:numel(glib(1))
    gele = get(glib(1),i);
    gc = xy(gele);
    x = gc{1}(:,1) - mybox(1);
    y = mybox(4) - gc{1}(:,2);
    polygon = Project.addMetalPolygonEasy(0,x,y);
    flagx1 = 0;
    flagx2 = 0;
    flagy1 = 0;
    flagy2 = 0;
    for j = 1:length(gc{1})
        if gc{1}(j,1) == mybox(1)
            if flagy1 == 0
                tempy = gc{1}(j,2);
                flagy1 = 1;
            else
                if tempy > gc{1}(j,2)
                    boundaryXL{end+1} = [gc{1}(j,2),tempy];
                else
                    boundaryXL{end+1} = [tempy,gc{1}(j,2)];
                end
                flagy1 = 0;
            end
        end
        if gc{1}(j,1) == mybox(3)
            if flagy2 == 0
                tempy = gc{1}(j,2);
                flagy2 = 1;
            else
                if tempy > gc{1}(j,2)
                    boundaryXR{end+1} = [gc{1}(j,2),tempy];
                else
                    boundaryXR{end+1} = [tempy,gc{1}(j,2)];
                end
                flagy2 = 0;
            end
        end
        if gc{1}(j,2) == mybox(2)
            if flagx1 == 0
                tempx = gc{1}(j,1);
                flagx1 = 1;
            else
                if tempx > gc{1}(j,1)
                    boundaryYB{end+1} = [gc{1}(j,1),tempx];
                else
                    boundaryYB{end+1} = [tempx,gc{1}(j,1)];
                end
                flagx1 = 0;
            end
        end
        if gc{1}(j,2) == mybox(4)
            if flagx2 == 0
                tempx = gc{1}(j,1);
                flagx2 = 1;
            else
                if tempx > gc{1}(j,1)
                    boundaryYT{end+1} = [gc{1}(j,1),tempx];
                else
                    boundaryYT{end+1} = [tempx,gc{1}(j,1)];
                end
                flagx2 = 0;
            end
        end
    end
end

if length(boundaryXL) ~= 1
    boundarylength = length(boundaryXL);
    for i = 2:(boundarylength-1)
        t = i;
        for j = (i+1):boundarylength
            if boundaryXL{t}(1) > boundaryXL{j}(1)
                t = j;
            end
        end
        if t ~= i
            boundaryXL{t} = boundaryXL{t} + boundaryXL{i};
            boundaryXL{i} = boundaryXL{t} - boundaryXL{i};
            boundaryXL{t} = boundaryXL{t} - boundaryXL{i};
        end
    end
    i = 2;
    while i < boundarylength - 1
        if boundaryXL{i+1}(1) - boundaryXL{i}(2) > 0.001
            Project.addPortAtLocation(0,mybox(4)-(boundaryXL{i+1}(1)+boundaryXL{i+1}(2))/2);
            i = i + 1;
        end
        i = i + 1;
    end
end
if length(boundaryXR) ~= 1
    boundarylength = length(boundaryXR);
    for i = 2:(boundarylength-1)
        t = i;
        for j = (i+1):boundarylength
            if boundaryXR{t}(1) > boundaryXR{j}(1)
                t = j;
            end
        end
        if t ~= i
            boundaryXR{t} = boundaryXR{t} + boundaryXR{i};
            boundaryXR{i} = boundaryXR{t} - boundaryXR{i};
            boundaryXR{t} = boundaryXR{t} - boundaryXR{i};
        end
    end
    i = 2;
    while i < boundarylength - 1
        if boundaryXR{i+1}(1) - boundaryXR{i}(2) > 0.001
            Project.addPortAtLocation(mybox(3)-mybox(1),mybox(4)-(boundaryXR{i+1}(1)+boundaryXR{i+1}(2))/2);
            i = i + 1;
        end
        i = i + 1;
    end
end

if length(boundaryYB) ~= 1
    boundarylength = length(boundaryYB);
    for i = 2:(boundarylength-1)
        t = i;
        for j = (i+1):boundarylength
            if boundaryYB{t}(1) > boundaryYB{j}(1)
                t = j;
            end
        end
        if t ~= i
            boundaryYB{t} = boundaryYB{t} + boundaryYB{i};
            boundaryYB{i} = boundaryYB{t} - boundaryYB{i};
            boundaryYB{t} = boundaryYB{t} - boundaryYB{i};
        end
    end
    i = 2;
    while i < boundarylength - 1
        if boundaryYB{i+1}(1) - boundaryYB{i}(2) > 0.001
            Project.addPortAtLocation((boundaryYB{i+1}(1)+boundaryYB{i+1}(2))/2-mybox(1),0);
            i = i + 1;
        end
        i = i + 1;
    end
end
if length(boundaryYT) ~= 1
    boundarylength = length(boundaryYT);
    for i = 2:(boundarylength-1)
        t = i;
        for j = (i+1):boundarylength
            if boundaryYT{t}(1) > boundaryYT{j}(1)
                t = j;
            end
        end
        if t ~= i
            boundaryYT{t} = boundaryYT{t} + boundaryYT{i};
            boundaryYT{i} = boundaryYT{t} - boundaryYT{i};
            boundaryYT{t} = boundaryYT{t} - boundaryYT{i};
        end
    end
    i = 2;
    while i < boundarylength - 1
        if boundaryYT{i+1}(1) - boundaryYT{i}(2) > 0.001
            Project.addPortAtLocation((boundaryYT{i+1}(1)+boundaryYT{i+1}(2))/2-mybox(1),mybox(4)-mybox(2));
            i = i + 1;
        end
        i = i + 1;
    end
end

Project.changePolygonType(polygon,'Lossless');
Project.addAbsFrequencySweep(freqstart,freqstop);
Project.ControlBlock.TargetAbs = freqabs;
Project.ControlBlock.Speed = 2;

% Write the project to the file
Project.saveAs('Demo2.son');

Project.openInSonnet();

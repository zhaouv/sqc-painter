function aPort=addPortCocalibrateAtLocation(obj,theXCoordinate,theYCoordinate, theLevel)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % This method will add an standard port
    %  to the project by specifying an X and Y coordinate.
    %  When this occurs the function will find the closest
    %  polygon side and place the port there. If the
    %  closest side for the port it more than 5% of the
    %  average of the length and width of the box then
    %  the port will not be placed and an error will be thrown.
    %
    %  Parameters
    %     1) The X coordinate for the port
    %     2) The Y coordinate for the port
    %     3) The level for the port (optional)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    if nargin == 3 || nargin == 4

        % Find a valid Port Number
        aPortNumber=1;
        for iCounter=1:length(obj.ArrayOfPorts)
            if aPortNumber==obj.ArrayOfPorts{iCounter}.PortNumber
                aPortNumber=aPortNumber+1;
                iCounter=1;  % Reset the counter to start at the beginning of the loop again.
            end
        end

        % find the closest edge to where was clicked to find the connected polygon
        aLengthOfPolygonArray=length(obj.ArrayOfPolygons);

        % loop for all the polygons in the array
        aBestDistance=inf;

        % make the new port if it is close to the polygon. if it is really far away then
        % dont make a port because the user probably misclicked. we will define
        % far away as more than 5% of the box (width+length)/2
        aDistanceThreshold=(obj.SonnetBox.XWidthOfTheBox+obj.SonnetBox.YWidthOfTheBox)/2*.05;

        for iCounter=1:aLengthOfPolygonArray

            % if the polygon is not on the same level as specified then skip it
            if nargin == 4 && theLevel ~= obj.ArrayOfPolygons{iCounter}.MetalizationLevelIndex
                continue;
            end

            % if the polygon is dielectric brick then ignore it
            if strcmpi(obj.ArrayOfPolygons{iCounter}.Type,'BRI POLY')==1
                continue;
            end

            % loop for all the sides in an polygon
            for jCounter=1:length(obj.ArrayOfPolygons{iCounter}.XCoordinateValues)-1

                aCoordinate1=[obj.ArrayOfPolygons{iCounter}.XCoordinateValues{jCounter},...
                    obj.ArrayOfPolygons{iCounter}.YCoordinateValues{jCounter}, 0];
                aCoordinate2=[obj.ArrayOfPolygons{iCounter}.XCoordinateValues{jCounter+1},...
                    obj.ArrayOfPolygons{iCounter}.YCoordinateValues{jCounter+1}, 0];
                aCenterPointX=mean([aCoordinate1(1) aCoordinate2(1)]);
                aCenterPointY=mean([aCoordinate1(2) aCoordinate2(2)]);

                % find the distance from the center point to our new point
                aDistance = sqrt((aCenterPointX-theXCoordinate)^2+(aCenterPointY-theYCoordinate)^2);

                % if this distance is closer than the best distance so far
                % then store it (unless it is more than 5% away)
                if aDistance < aBestDistance && aDistance <= aDistanceThreshold
                    aBestDistance=aDistance;
                    aBestVertex=jCounter;
                    aBestPolygon=obj.ArrayOfPolygons{iCounter};
                end

            end

        end

        if aBestDistance < inf

            if aBestDistance <= aDistanceThreshold

                % find the coordinates at which to place the port (the center of the vertex)
                aPortXLocation=(aBestPolygon.XCoordinateValues{aBestVertex}+aBestPolygon.XCoordinateValues{aBestVertex+1})/2;
                aPortYLocation=(aBestPolygon.YCoordinateValues{aBestVertex}+aBestPolygon.YCoordinateValues{aBestVertex+1})/2;

                % make the port
                aPort=obj.addPortCocalibrated(aBestPolygon,'A',aBestVertex,50,0,0,0);

            else
                error('Requested port location not near polygon edge.');
            end
        end

        % If we recieved an improper number of arguments
    else
        disp('Improper number of arguments.  See help.');
    end

end
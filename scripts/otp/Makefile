town := denver


.PHONY: otp


otp:
	# create directory for data and config
	-mkdir $(town)
	cp build-config.jsonc $(town)/build-config.json
	# download OSM
	if [ ! -f $(town)/osm.pbf ]; then \
        curl -C - -L -k https://download.geofabrik.de/north-america/us/colorado-latest.osm.pbf -o $(town)/osm.pbf; \
    fi
	# download GTFS
	# this is the latest gtfs file
	#curl -L -k https://www.rtd-denver.com/files/gtfs/google_transit.zip -o $(town)/denver-rtd-gtfs.zip
	# 2022
	#curl -C - -L -k -H "Accept: application/zip" https://web.archive.org/web/20220308061530/https://www.rtd-denver.com/files/gtfs/google_transit.zip -o $(town)/denver-2022-rtd-gtfs.zip
	#curl -L -k https://web.archive.org/web/20220308061530if_/https://www.rtd-denver.com/files/gtfs/google_transit.zip -o $(town)/denver-2022-rtd-gtfs.zip
	# build graph and save it onto the host system via the volume
	@echo "Go to Docker Desktop and change resource to maximum memory and swap."
	docker run --rm \
		-e JAVA_TOOL_OPTIONS='-Xmx32g' \
		-v ./$(town):/var/opentripplanner docker.io/opentripplanner/opentripplanner:latest --build --save
	# load and serve graph
	docker run -it --rm -p 9999:8080 \
		-e JAVA_TOOL_OPTIONS='-Xmx32g' \
		-v ./$(town):/var/opentripplanner \
		docker.io/opentripplanner/opentripplanner:latest --load --serve

manual:
	java -Xmx2G -jar otp-2.6.0-shaded.jar --build --serve /home/username/otp
	# osmium extract --bbox=-123.043,45.246,-122.276,45.652 -o portland.pbf oregon-latest.osm.pbf

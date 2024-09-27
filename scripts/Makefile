town := denver


.PHONY: otp


otp:
	# create directory for data and config
	-mkdir $(town)
	cp build-config.jsonc $(town)/build-config.json
	# download OSM
	curl -C - -L -k https://download.geofabrik.de/north-america/us/colorado-latest.osm.pbf -o $(town)/osm.pbf  
	# download GTFS
	curl -C - -L -k https://www.rtd-denver.com/files/gtfs/google_transit.zip -o $(town)/denver-rtd-gtfs.zip
	# build graph and save it onto the host system via the volume
	@echo "Go to Docker Desktop and change resource to 16gb memory and 2gb swap"
	docker run --rm \
		--memory=8g \
		-e JAVA_OPTS='-Xmx8g' \
		-v ./$(town):/var/opentripplanner docker.io/opentripplanner/opentripplanner:latest --build --save
	# load and serve graph
	docker run -it --rm -p 9999:8080 \
		--memory=8g \
		-e JAVA_OPTS='-Xmx8g' \
		-v ./$(town):/var/opentripplanner \
		docker.io/opentripplanner/opentripplanner:latest --load --serve

manual:
	java -Xmx2G -jar otp-2.6.0-shaded.jar --build --serve /home/username/otp
	# osmium extract --bbox=-123.043,45.246,-122.276,45.652 -o portland.pbf oregon-latest.osm.pbf

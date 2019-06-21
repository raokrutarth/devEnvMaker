# Network
NET := halonn
SUBNET := 172.20.0.0/24


RAW_IMAGE := /aruba/pub/cit/halon/LEVEL1_P4__GVT_P4/75836/genericx86-p4_essw_cit_master_20190619_081240_2364c37.tar.gz
HALON_IMAGE := haloni

# Halon
HALON_CONTAINER := halonc
HALON_IP := 172.20.0.4
WEBUI_PORT := 443
OVSDB_PORT := 6640


# halon-benchmark realted ports
PROC_EXPORTER_PORT = 35001
LOG_EXPORTER_PORT = 35002
DEV_EXPORTER_PORT = 35003
CONFIG_EXPORTER_PORT = 35005

# device name can be any string
DEVICE_NAME := 5555


rm-net:
	-@docker network rm $(NET)

add-net:
	docker network create --driver bridge --subnet=$(SUBNET) $(NET)

halon-image:
	@printf "\nImage: "
	@echo $(RAW_IMAGE)

	cat $(RAW_IMAGE) | docker import - $(HALON_IMAGE)

# --publish hostPort:conPort
halon-run:
	docker run \
		--privileged \
		--detach \
		--publish $(WEBUI_PORT):$(WEBUI_PORT) \
		--expose 22 \
		--expose $(PROC_EXPORTER_PORT) \
		--expose $(LOG_EXPORTER_PORT) \
		--expose $(DEV_EXPORTER_PORT) \
		--expose $(CONFIG_EXPORTER_PORT) \
		--expose $(OVSDB_PORT) \
		--net $(NET) \
		--ip $(HALON_IP) \
		--name $(HALON_CONTAINER) $(HALON_IMAGE) /sbin/init &


# NOTE: `docker exec` commands sometimes give "error: process ID out of range". command still succedes.
# 1) need to remove old ssh key if there is one for the specific IP address.
# 2) enable ssh & set password
# 3) set hostname so it's easy to identify the device from the prompt
halon-provision:

	HALON_IP=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(HALON_CONTAINER))
	-@ssh-keygen -f "/users/raokru/.ssh/known_hosts" -R $(HALON_IP)

	sleep 5s
	-@docker exec $(HALON_CONTAINER) vtysh -c "configure" -c "interface mgmt" -c "ip static $(HALON_IP)/16" -c "no shutdown" &> /dev/null
	-@docker exec $(HALON_CONTAINER) vtysh -c "configure" -c "ssh server vrf mgmt" &> /dev/null
	-@docker exec $(HALON_CONTAINER) vtysh -c "configure" -c "user admin password plaintext admin" &> /dev/null
	-@docker exec $(HALON_CONTAINER) vtysh -c "configure" -c "hostname $(DEVICE_NAME)" &> /dev/null


clean-container:
	-@docker rm -f $(HALON_CONTAINER)

clean-image:
	-@docker rmi -f $(HALON_IMAGE)

ip-print:
	@printf "\nIP address: \n"
	docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(HALON_CONTAINER)
	@printf "\n\n"


# build the container & provision it
halon: clean add-net halon-run halon-provision ip-print

# remove ...
clean: clean-container rm-net

# remove ...
cleani: clean-container clean-image rm-net

all: cleani halon-image halon


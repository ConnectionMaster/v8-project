V8_SOURCE_DIR := third_party/v8
REVISION := $(shell python3 get-revision.py webview stable)
SHORT_REVISION := $(shell echo $(REVISION)|cut -b1-8)
BASE_NAME := v8-$(strip $(SHORT_REVISION))
SUPPORTED_ANDROID_ARCHS := arm arm64 ia32 x64
SUPPORTED_LINUX_ARCHS := ia32 x64
LIBRARY_FILES := $(foreach arch,$(SUPPORTED_ANDROID_ARCHS),android-$(arch)-release.tar.xz) \
	$(foreach arch,$(SUPPORTED_LINUX_ARCHS),$(foreach config,debug release,linux-$(arch)-$(config).tar.xz))
INCLUDES_FILE := include.tar.xz
TARGETS := build/$(INCLUDES_FILE) \
	$(foreach f,$(LIBRARY_FILES),build/$(f)) \
	build/info
URLS := $(foreach f,$(INCLUDES_FILE) $(LIBRARY_FILES),https://v8.eyeofiles.com/$(BASE_NAME)/$(f))

get_arch_name=$(shell echo $1|tr "/." "-"|cut -f3 -d'-')
get_os_name=$(shell echo $1|tr "/." "-"|cut -f2 -d'-')
get_configuration_name=$(shell echo $1|tr "/." "-"|cut -f4 -d'-')

all: $(TARGETS)

check_up_to_date:
	@python3 remote-files-exist.py $(URLS)

debug:
	$(foreach v,$(MAKECMDGOALS), \
		$(if $(filter debug,$v),,$(warning $v = $($v))))

clean:
	@rm -rf build/

build/%.tar.xz: arch=$(call get_arch_name,$@)
build/%.tar.xz: os=$(call get_os_name,$@)
build/%.tar.xz: configuration=$(call get_configuration_name,$@)
build/%.tar.xz: $(V8_SOURCE_DIR)
	python3 build.py $(os) $(arch) $(configuration)
	tar cJf $@ -C build/$(os).$(arch).$(configuration)/obj libv8_monolith.a

build/$(INCLUDES_FILE): $(V8_SOURCE_DIR)
	@mkdir -p build
	@tar cJf $@ -C third_party/v8 include

build/info:
	mkdir -p build
	echo $(REVISION) > $@

$(V8_SOURCE_DIR):
	@python3 sync.py $(REVISION)

# the prerequisites match
# https://gitlab.com/eyeo/docker/-/tree/master/v8-project_gitlab-runner
.PHONY: build_prerequisites
build_prerequisites: check_prerequisites
	sudo dpkg --add-architecture i386
	sudo apt-get update
	sudo apt-get install -yyq build-essential libgtk2.0-dev libc6:i386 xz-utils

.PHONY: check_prerequisites
check_prerequisites:
	sudo apt-get update
	sudo apt-get install -yyq python3.6 python3-requests

.PHONY: get_base_name
get_base_name:
	@echo $(BASE_NAME)

.PHONY: $(V8_SOURCE_DIR) clean debug

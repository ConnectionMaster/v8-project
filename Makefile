V8_SOURCE_DIR := third_party/v8
REVISION := $(shell python3 get-revision.py webview stable)
SHORT_REVISION := $(shell echo $(REVISION)|cut -b1-8)
BASE_NAME := v8-$(strip $(SHORT_REVISION))
SUPPORTED_ANDROID_ARCHS := arm arm64 ia32 x64
LIBRARY_FILES := $(foreach arch,$(SUPPORTED_ANDROID_ARCHS),$(BASE_NAME)-$(arch)-android.tar.xz)
INCLUDES_FILE := $(BASE_NAME)-includes.tar.xz
TARGETS := build/$(INCLUDES_FILE) $(foreach f,$(LIBRARY_FILES),build/$(f))
URLS := $(foreach f,$(INCLUDES_FILE) $(LIBRARY_FILES),https://v8.eyeofiles.com/$(f))

get_arch_name=$(shell echo $1|cut -f3 -d'-')

all: $(TARGETS)

update: needs_update all

needs_update:
	@python3 files-do-not-exist.py $(URLS)

debug:
	$(foreach v,$(MAKECMDGOALS), \
		$(if $(filter debug,$v),,$(warning $v = $($v))))

clean:
	@rm -rf build/

build/v8-%-android.tar.xz: arch=$(call get_arch_name,$@)
build/v8-%-android.tar.xz: $(V8_SOURCE_DIR)
	@python3 build.py android $(arch) release
	tar cJf $@ -C build/android.$(arch).release/obj libv8_monolith.a

build/$(INCLUDES_FILE): $(V8_SOURCE_DIR)
	@mkdir -p build
	@tar cJf $@ -C third_party/v8 include

$(V8_SOURCE_DIR):
	@python3 sync.py $(REVISION)

.PHONY: $(V8_SOURCE_DIR) clean debug

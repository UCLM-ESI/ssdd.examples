SUBDIRS = $(dir $(shell find -mindepth 2 -name Makefile))

clean:
	for dir in $(SUBDIRS); do \
	    $(MAKE) -C $$dir clean; \
        done

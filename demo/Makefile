.PHONY: clean
clean:
	rm -rf output

.PHONY: demo
demo: clean
	uv run reloci --dryrun source output
	uv run reloci source output

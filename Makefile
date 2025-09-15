Science_CommunityDir := Science_Community
Science_CommunitySources := 2025-09-12-LlamaIndexScienceCommunityChat 2025-09-12-LlamaBedRock
source += $(foreach jupfile,$(Science_CommunitySources), $(Science_CommunityDir)/$(jupfile))

files := $(foreach wrd,$(source),$(wrd).md)
all: $(files)

# Function to create ipynb --> md
define make-markdown
$2/$1.md : $2/$1.ipynb
	@echo "-------------------------"
	@echo "Converting $$< -> $$@"
	@echo "-------------------------"
	uv run jupyter nbconvert --HTMLExporter.sanitize_html=true $$< --to markdown \
		--TagRemovePreprocessor.remove_input_tags="['remove_input','remove_output']" \
		--NbConvertApp.output_files_dir=./assets/images/$1 \
		--ExtractOutputPreprocessor.output_filename_template='fig_{index}{extension}'
		
	sed -i '' -E 's/\x1B\[[0-9;]*[mK]//g' $$@
	sed -i '' -E 's/\(\.\/assets/\(\/assets/g' $$@
	cp $$@  ~/GitHub/ojitha.github.io/_drafts/

	# Check if folder exists and create if needed
	@if [ -d "./$2/assets/images/$1" ]; then \
		echo "--- Folder exists -----"; \
		if [ ! -d ~/GitHub/ojitha.github.io/assets/images/$1 ]; then \
			mkdir -p ~/GitHub/ojitha.github.io/assets/images/$1; \
		fi; \
		cp -r ./$2/assets/images/$1/* ~/GitHub/ojitha.github.io/assets/images/$1/; \
	else \
		echo "Folder does not exist"; \
	fi
endef

# Generate the rules for each source file
$(foreach element,$(Science_CommunitySources),$(eval $(call make-markdown,$(element),$(Science_CommunityDir))))

cleanmarkdown = $(shell rm $2/$1.md)	

# Clean target
clean:
	@echo "cleaning ..."
	$(foreach element,$(Science_CommunitySources),$(eval $(call cleanmarkdown,$(element),$(Science_CommunityDir))))


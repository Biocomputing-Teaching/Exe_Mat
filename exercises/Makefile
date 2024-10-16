# Variables
LATEXMK=latexmk
#LATEXMK_FLAGS=-pdf -interaction=nonstopmode -halt-on-error
SRC_DIR=./
COM_DIR=../common
FIG_DIR=../figures
BUILD_DIR=../build

# Common dependencies
COMMON=$(wildcard $(COM_DIR)/*.tex)

# Image dependencies
IMAGES=$(wildcard $(FIG_DIR)/*.png)

# LaTeX document names (without the .tex extension)
DOC_CAT=ExercicisResolts
DOC_ENG=SolvedExercises

# Targets
CAT_TARGET=$(BUILD_DIR)/$(DOC_CAT).pdf
ENG_TARGET=$(BUILD_DIR)/$(DOC_ENG).pdf

# Default target: build all PDFs or just one
all: cat eng


# Rule to build pdfs
$(BUILD_DIR)/%.pdf: $(SRC_DIR)/%.tex $(wildcard $(SRC_DIR)/*.tex) $(IMAGES) $(COMMON)
	@mkdir -p $(BUILD_DIR)
	$(LATEXMK) $(LATEXMK_FLAGS) -output-directory=$(BUILD_DIR) $(SRC_DIR)/$*.tex

cat: $(CAT_TARGET)
eng: $(ENG_TARGET)

# Clean all build files
clean:
	$(LATEXMK) -C -output-directory=$(BUILD_DIR) $(SRC_DIR)/$(DOC_CAT).tex
	$(LATEXMK) -C -output-directory=$(BUILD_DIR) $(SRC_DIR)/$(DOC_ENG).tex

cleanpdf:
	rm -rf $(BUILD_DIR)/*.pdf

.PHONY: all cat eng clean

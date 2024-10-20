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
DOC_OR=SolvedExercisesOR

# Targets
CAT_TARGET=$(BUILD_DIR)/$(DOC_CAT).pdf
ENG_TARGET=$(BUILD_DIR)/$(DOC_ENG).pdf
OR_TARGET=$(BUILD_DIR)/$(DOC_OR).pdf


# Default target: build all PDFs or just one
all: cat eng


# Rule to build pdfs
$(BUILD_DIR)/%.pdf: $(SRC_DIR)/%.tex $(wildcard $(SRC_DIR)/*.tex) $(IMAGES) $(COMMON)
	@mkdir -p $(BUILD_DIR)
	$(LATEXMK) $(LATEXMK_FLAGS) -output-directory=$(BUILD_DIR) $(SRC_DIR)/$*.tex

cat: $(CAT_TARGET)
eng: $(ENG_TARGET)
or: $(OR_TARGET)

# Clean all build files
clean:
	$(LATEXMK) -C -output-directory=$(BUILD_DIR) $(SRC_DIR)/$(DOC_CAT).tex
	$(LATEXMK) -C -output-directory=$(BUILD_DIR) $(SRC_DIR)/$(DOC_ENG).tex
	$(LATEXMK) -C -output-directory=$(BUILD_DIR) $(SRC_DIR)/$(DOC_OR).tex

cleanpdf:
	rm -rf $(BUILD_DIR)/*.pdf

.PHONY: all cat eng or clean

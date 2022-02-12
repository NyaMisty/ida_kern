IDACLANG := idaclang
TILIB64 := tilib64
IDACLANG_ARGS += --idaclang-log-all
IDACLANG_ARGS += --idaclang-tildesc $(TIL_DESC)

CLANG_ARGV += -ferror-limit=50

INPUT_FILE := ../idasdk.h
BASE_FILE := ../base.h

all: $(TIL_NAME)
.PHONY: all $(TIL_NAME) clean
$(TIL_NAME): $(TIL_NAME).til $(TIL_NAME).py

base.til: $(BASE_FILE)
	$(IDACLANG) $(IDACLANG_ARGS) --idaclang-tilname base --idaclang-tildesc BaseTIL $(CLANG_ARGV) $(BASE_FILE) > base.log

$(TIL_NAME).til: $(TIL_NAME).mak $(INPUT_FILE) base.til
	$(IDACLANG) $(IDACLANG_ARGS) --idaclang-tilname $(TIL_NAME) --idaclang-tildesc $(TIL_DESC) $(CLANG_ARGV) $(INPUT_FILE) > $(TIL_NAME).log
	$(TILIB64) -bbase.til -u+ $(TIL_NAME).til

$(TIL_NAME).py: $(TIL_NAME).til
	$(TILIB64) -lc $(TIL_NAME).til > $(TIL_NAME).h
	python3 ../gen_interop_til.py $(TIL_NAME).h $@

clean:
	rm -rf *.til *.txt *.log

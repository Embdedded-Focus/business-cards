PDF := business_card_embedded_focus.pdf
all: $(PDF)

qr_code_rpoisel.svg: rpoisel.vcf ef-qr.py
	python ef-qr.py -o $@ -i $<

%.pdf: %.svg
	inkscape --export-type=pdf --export-area-page -o $@ $^

.PHONY: clean
clean:
	rm -f $(PDF)

PRES = pres.ipynb
SRC = $(shell find src -name "*.md" | sort -n)

GEN = $(PRES)

$(PRES):	$(SRC)
		lucina -o $@ $^

pres:		$(PRES)

clean:
		rm -f $(GEN)

re:		clean $(GEN)

run:		$(PRES)
		jupyter-notebook $<

.PHONY:		pres clean re run

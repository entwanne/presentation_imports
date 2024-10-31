PRES = pres.ipynb
SRC = $(shell find src -name "*.md" | sort -n)

GEN = $(PRES)

$(PRES):	$(SRC)
		lucina -o $@ $^ --no-autolaunch

pres:		$(PRES)

clean:
		rm -f $(GEN)

re:		clean $(GEN)

run:		$(PRES)
		jupyter-notebook --browser=firefox $<

.PHONY:		pres clean re run

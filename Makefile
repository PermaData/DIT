TESTPATH = .\tests

.PHONY: clean test

clean:
	del /s *.pyc $(TESTPATH)\*.in *.out
	
test:
	nosetests $(TESTPATH)

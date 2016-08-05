TESTPATH = .\tests
SCRIPTPATH = C:\Users\Nicholas Thurmes\Anaconda2\Scripts

.PHONY: clean test check

clean:
	del /s *.pyc $(TESTPATH)\*.in *.out

test:
	$(SCRIPTPATH)\nosetests.exe $(TESTPATH)
	
check:
	$(SCRIPTPATH)\pep8.exe $(TESTPATH)
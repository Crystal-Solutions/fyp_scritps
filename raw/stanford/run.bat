java -cp ..\..\tools\stanford-ner-2016-10-31\stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier target/1.ner-model.ser.gz -textFile ..\..\data\text\feedback_cs2012_1.txt > target/test_result/cs2012_1.txt

java -cp ..\..\tools\stanford-ner-2016-10-31\stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier target/1.ner-model.ser.gz -textFile ..\..\data\text\feedback_cs2012_2.txt > target/test_result/cs2012_2.txt

java -cp ..\..\tools\stanford-ner-2016-10-31\stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier target/1.ner-model.ser.gz -textFile ..\..\data\text\feedback_cs2202_1.txt > target/test_result/cs2202_1.txt

java -cp ..\..\tools\stanford-ner-2016-10-31\stanford-ner.jar edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier target/1.ner-model.ser.gz -textFile ..\..\data\text\feedback_cs2202_2.txt > target/test_result/cs2202_2.txt
pause
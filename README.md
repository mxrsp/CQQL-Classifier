# CQQL-Classifier
This repository hosts an implementation of a classifier, that is based on the Commuting Quantum Query Language CQQL.
It is based on the paper "Generating CQQL conditions from classifying CNNs" from Ingo Schmitt(see https://opus4.kobv.de/opus4-btu/frontdoor/index/index/year/2021/docId/5550).

CQQL itself is inspired by quantum logic and it's conditions obey the rules of Boolean algebra.
They way the classifier works, is that all terms that fulfill a certain condition(in that case class 1) are extracted using training data.
After the extraction, these terms can be used to classify.

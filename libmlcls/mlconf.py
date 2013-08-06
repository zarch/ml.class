import mlpy


BEST = {'knn': mlpy.KNN(1),
        'tree': mlpy.ClassTree(stumps=0, minsize=0),
        'svm': mlpy.LibSvm(svm_type='c_svc',
                           kernel=mlpy.KernelGaussian(10), C=10**4)
}


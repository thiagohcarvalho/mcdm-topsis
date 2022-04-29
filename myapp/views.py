from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Document
from .forms import DocumentForm
from .topsis import Topsis
import csv
import re
import os


def my_view(request):
    message = 'Upload as many files as you want!'
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            return redirect('topsis-score')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form,
               'message': message}
    return render(request, 'list.html', context)


def topsis_score(request):
    alternative_list = []
    matrix = []
    weight = []
    criteria = []
    if request.method == 'POST':  # if user is reusing an already uploaded file
        doc = request.POST.get("filename")  # request.post.get returns a dict
        doc = os.path.abspath(os.getcwd()) + doc
    else:  # if user is sending a new file
        document = Document.objects.latest('id')
        doc = document.docfile.path
    while True:
        file_extension = os.path.splitext(doc)
        if file_extension[1] == ".csv":
            arq = open(doc, 'r')
            arquivo = csv.reader(arq, delimiter=',')
            for row in arquivo:
                if row[0] == 'criteria':
                    del row[0]
                    for c in row:
                        if c == 'max':
                            criteria.append(True)
                        elif c == 'min':
                            criteria.append(False)

                elif row[0] == '':
                    pass
                elif row[0] == 'pesos':
                    del row[0]
                    for s in row:
                        n = re.findall(r'\d+\,*\d*', s)
                        string = ''
                        for p in n:
                            string += p
                        string = string.replace(',', '.')
                        weight.append(float(string))
                else:
                    alternative_list.append(row[0])
                    del row[0]
                    temp = []
                    for s in row:
                        try:
                            temp.append(float(s))
                        except:
                            n = re.findall(r'\d+\,*\d*', s)
                            string = ''
                            for p in n:
                                string += p
                            string = string.replace(',', '.')
                            temp.append(float(string))
                    matrix.append(temp)
            arq.close()
            break
        else:
            return redirect('my-view')

    topsis = Topsis(matrix, criteria, weight, alternative_list)

    normalization_scores = topsis.normalize_matrix()
    weighted_matrix = topsis.weight_matrix()
    step4 = topsis.best_worst_ideal_solution()
    find_distance = topsis.find_distance()
    find_D = topsis.find_similarity_worse_decision()
    score = topsis.ranking_by_worst()
    score_inverted = topsis.ranking_by_worst_inverted()

    context = {'normalization_scores': normalization_scores, 'weighted_matrix': weighted_matrix, 'step4': step4,
               'find_distance': find_distance, 'find_D': find_D, 'ranking': score, 'ranking_inverted': score_inverted}
    return render(request, 'score.html', context)


def delete_files(request):
    if request.method == "POST":
        Document.objects.all().delete()
    return redirect('my-view')

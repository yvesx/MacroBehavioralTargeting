%% test performance of post type classification
%% using user-response as cluster 
%% challenges: 
%% *training set small: have to do brand by brand. a brand
%% has like 100~400 posts a year
%% *label matrix is sparse: PostUsers
%% *feature is sparse

clear all;
load samsung_matlab_matrix;
cv=20;
num_clst = 2; %% why using 2 clsts is *much* better than 3 clusters
dense = double(dense);
ftr_lst = double(ftr_lst);
clst = kmeans(dense,num_clst,'distance','cosine','emptyaction','drop');
%% using manhattan distance get very bad(small) clusters.
%% this is b/c sparsity varies too much from post to post
%% correlation distance is fine. Hamming is useless here

%% why w/o feedback always performs better?

%% first validate using full features lists
err_cum = 0;
for i = 1:cv
    net = patternnet(10);
    x = ftr_lst';
    t = clst';
    [net,tr] = train(net,x,t);nntraintool('close');
    testX = x(:,tr.testInd);
    testT = t(:,tr.testInd);
    testY = net(testX);
    testY = round(testY);
    err_cum = err_cum + sum(min(abs(testT-testY),1))/length(testY);
end
display('mis-classified w/ feedback');
err_cum/cv

%% then validate with only non-feedback features
err_cum = 0;
for i = 1:cv
    ftr_lst(:,[1 5 21]) = 0;
    net = patternnet(10);
    x = ftr_lst';
    t = clst';
    [net,tr] = train(net,x,t);nntraintool('close');
    testX = x(:,tr.testInd);
    testT = t(:,tr.testInd);
    testY = net(testX);
    testY = round(testY);

    
    err_cum = err_cum + sum(min(abs(testT-testY),1))/length(testY);
end
display('mis-classified w/o feedback');
err_cum/cv
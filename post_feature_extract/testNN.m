%% test performance of post type classification
%% using user-response as cluster 
%% challenges: 
%% *training set small: have to do brand by brand. a brand
%% has like 100~400 posts a year
%% *label matrix is sparse: PostUsers
%% *feature is sparse

clear all;
load bmw_matlab_matrix;
cv=10
num_clst = 3;
dense = double(dense);
ftr_lst = double(ftr_lst);
clst = kmeans(dense,num_clst,'distance','cosine');

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
    display('mis-classified w/ feedback');
    err_cum = err_cum + sum(abs(testT-testY))/length(testY);
end
err_cum/cv;
ftr_lst(:,[1 5 21]) = 0;
net = patternnet(10);
x = ftr_lst';
t = clst';
[net,tr] = train(net,x,t);nntraintool('close');
testX = x(:,tr.testInd);
testT = t(:,tr.testInd);
testY = net(testX);
testY = round(testY);

display('mis-classified w/o feedback');
sum(abs(testT-testY))/length(testY)
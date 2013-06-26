clear all
close all
load fisheriris
load bmw_matlab_matrix
load bmw_cidx_nn
labelx = '#Shared';
labely = '#Comments';
labelz = '#Likes';
ftr1='SL';ftr2='SW';
ftr3='PL';ftr4='PW';
clstr1='NewProduct Posts';clstr2='Discount Posts';clstr3='Greeting Posts';
clstrs={clstr1, clstr2, clstr3};
meas = double(ftr_lst);
dense = double(dense);
[r c] = size(meas);
ptsymb = {'bs','r^','md','go','c+'};
lnsymb = {'b-','r-','m-'};


%% three clusters with cosine distance
%[cidxCos,cmeansCos] = kmeans(meas,3,'emptyaction','drop');
[cidxCos,cmeansCos] = kmeans(dense,3,'distance','cosine','emptyaction','drop');
cidxCos = cidx_nn;


subplot(1,1,1);
for i = 1:3
    clust = find(cidxCos==i);
    h=plot3(meas(clust,1),meas(clust,5),meas(clust,21),ptsymb{i},'MarkerSize', 8);
    hold on
end
xlabel(labelx); ylabel(labely); zlabel(labelz);
view(-137,10);
grid on
%sidx = grp2idx(species);
sidx = kmeans(dense,3,'distance','cosine','emptyaction','drop');
miss = find(cidxCos ~= sidx);
plot3(meas(miss,1),meas(miss,5),meas(miss,21),'k*','MarkerSize', 6);
legend({clstr1,clstr2,clstr3});
hold off
figure

cosD = pdist(meas,'cosine');
clustTreeCos = linkage(cosD,'average');
[h,nodes] = dendrogram(clustTreeCos,0);
set(gca,'TickDir','out','TickLength',[.002 0],'XTickLabel',[]);
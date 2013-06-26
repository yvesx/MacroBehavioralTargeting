clear all
close all
load fisheriris
load samsung_matlab_matrix
labelx = '#Shared';
labely = '#Comments';
labelz = '#Likes';
ftr1='SL';ftr2='SW';
ftr3='PL';ftr4='PW';
clstr1='NewProduct Posts';clstr2='Discount Posts';clstr3='Greeting Posts';
clstrs={clstr1, clstr2, clstr3};
meas = double(dense);
meas = double(ftr_lst);
dense = double(dense);
[r c] = size(meas);
ptsymb = {'bs','r^','md','go','c+'};
lnsymb = {'b-','r-','m-'};

%% three clusters
[cidx3,cmeans3,sumd3] = kmeans(meas,3,'distance','cosine' ,'replicates',2,'display','final');
[silh3,h] = silhouette(meas,cidx3,'cosine');
for i = 1:3
    clust = find(cidx3==i);
    plot3(meas(clust,1),meas(clust,5),meas(clust,21),ptsymb{i});
    hold on
end
plot3(cmeans3(:,1),cmeans3(:,5),cmeans3(:,21),'ko');
plot3(cmeans3(:,1),cmeans3(:,5),cmeans3(:,21),'kx');
hold off
xlabel(labelx); ylabel(labely); zlabel(labelz);
view(-137,10);
grid on
figure

%% three clusters with cosine distance
[cidxCos,cmeansCos] = kmeans(meas,3,'dist','cos');
[silhCos,h] = silhouette(meas,cidxCos,'cos');
for i = 1:3
    clust = find(cidxCos==i);
    plot3(meas(clust,1),meas(clust,5),meas(clust,21),ptsymb{i});
    hold on
end
hold off
xlabel(labelx); ylabel(labely); zlabel(labelz);
view(-137,10);
grid on
figure

%% thnunder plot

names = {ftr1,ftr2,ftr3,ftr4};
meas0 = meas ./ repmat(sqrt(sum(meas.^2,2)),1,c);
ymin = min(min(meas0));
ymax = max(max(meas0));
for i = 1:3
    subplot(1,3,i); plot(meas0(cidxCos==i,:)',lnsymb{i});
    hold on; plot(cmeansCos(i,:)','k-','LineWidth',2); hold off;
    title(clstrs(i));
    set(gca,'Xlim',[.9 4.1],'XTick',1:4,'XTickLabel',names,'YLim',[ymin ymax])
end
figure

subplot(1,1,1);
for i = 1:3
    clust = find(cidxCos==i);
    plot3(meas(clust,1),meas(clust,2),meas(clust,3),ptsymb{i});
    hold on
end
xlabel(labelx); ylabel(labely); zlabel(labelz);
view(-137,10);
grid on
sidx = grp2idx(species);
miss = find(cidxCos ~= sidx);
%sidx = grp2idx(species);
sidx = kmeans(dense,3,'distance','cosine','emptyaction','drop');miss = find(cidxCos ~= sidx);
plot3(meas(miss,1),meas(miss,2),meas(miss,3),'k*');
legend({clstr1,clstr2,clstr3});
hold off
figure

cosD = pdist(meas,'cosine');
clustTreeCos = linkage(cosD,'average');
[h,nodes] = dendrogram(clustTreeCos,0);
set(gca,'TickDir','out','TickLength',[.002 0],'XTickLabel',[]);
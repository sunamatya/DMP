data1_1=READ("1_1");
data1_2=READ("1_2");
data1_3=READ("1_3");
data1_4=READ("1_4");

data2_1=READ("2_1");
data2_3=READ("2_3");
data2_4=READ("2_4");
%% IMU plots
% subplot(2,4,1)
% plot(data1_1.IMU(:,1))
% subplot(2,4,2)
% plot(data1_2.IMU(:,1))
% subplot(2,4,3)
% plot(data1_3.IMU(:,1))
% subplot(2,4,4)
% plot(data1_4.IMU(:,1))
% subplot(2,4,5)
% plot(data2_1.IMU(:,1))
% subplot(2,4,7)
% plot(data2_3.IMU(:,1))
% subplot(2,4,8)
% plot(data2_4.IMU(:,1))
%%  Force plots
figure(1)
subplot(2,4,1)
plot(data1_1.Fi(:,1)); hold on; ylim([-5 50]); title('1-1'); xlabel('Samples'); ylabel('Force (N)')
subplot(2,4,2)
plot(data1_2.Fi(:,1)); hold on; ylim([-5 50]); title('1-2'); xlabel('Samples'); ylabel('Force (N)')
subplot(2,4,3)
plot(data1_3.Fi(:,1)); hold on; ylim([-5 50]); title('1-3'); xlabel('Samples'); ylabel('Force (N)')
subplot(2,4,4)
plot(data1_4.Fi(:,1)); hold on; ylim([-5 50]); title('1-4'); xlabel('Samples'); ylabel('Force (N)')
subplot(2,4,5)
plot(data2_1.Fi(:,1)); hold on; ylim([-5 50]); title('2-1'); xlabel('Samples'); ylabel('Force (N)')
subplot(2,4,7)
plot(data2_3.Fi(:,1)); hold on; ylim([-5 50]); title('2-3'); xlabel('Samples'); ylabel('Force (N)')
subplot(2,4,8)
plot(data2_4.Fi(:,1)); hold on; ylim([-5 50]); title('2-4'); xlabel('Samples'); ylabel('Force (N)')
csvwrite('Force.csv',data2_4.Fi(:,1));
%% 
Ang1_1=(data1_1.IMU(:,1)-mean(data1_1.IMU(20:300,1)))*pi/180;
Ang2_1=(data2_1.IMU(:,1)-mean(data2_1.IMU(20:300,1)))*pi/180;
Ang1_2=(data1_2.IMU(:,1)-mean(data1_2.IMU(20:300,1)))*pi/180;
Ang1_3=(data1_3.IMU(:,1)-mean(data1_3.IMU(20:300,1)))*pi/180;
Ang1_4=(data1_4.IMU(:,1)-mean(data1_4.IMU(20:300,1)))*pi/180;
Ang2_3=(data2_3.IMU(:,1)-mean(data2_3.IMU(20:300,1)))*pi/180;
Ang2_4=(data2_4.IMU(:,1)-mean(data2_4.IMU(20:300,1)))*pi/180;

Fi_N_11=(sin(Ang1_1));
Fi_N_12=(sin(Ang1_2));
Fi_N_13=(sin(Ang1_3));
Fi_N_14=sin(Ang1_4);
Fi_N_21=sin(Ang2_1);
Fi_N_23=sin(Ang2_3);
Fi_N_24=sin(Ang2_4);

%%
figure(2);
subplot(2,4,1)
plot(data1_1.Encr(:,1))
subplot(2,4,2)
plot(data1_2.Encr(:,1))
subplot(2,4,3)
plot(data1_3.Encr(:,1))
subplot(2,4,4)
plot(data1_4.Encr(:,1))
subplot(2,4,5)
plot(data2_1.Encr(:,1))
subplot(2,4,7)
plot(data2_3.Encr(:,1))
subplot(2,4,8)
plot(data2_4.Encr(:,1))







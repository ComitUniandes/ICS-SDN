load('stealth_att_fig')
formatSpec = '%f';
fsz = 10;
% No_attack
h1=figure(1)
set(gca, 'FontSize', fsz, 'LineWidth', 1.5); 
plot(n,abs_inp_ref(1,1:length(n)),'k--',...
     n,no_attack(1,1:length(n)),'b',...
     n,abs_inp_ref(2,1:length(n)),'k--',...
     n,no_attack(2,1:length(n)),'r',...
     n,no_attack(3,1:length(n)),'m',...
     'LineWidth',2),grid
 
g = legend('Tank 1 Level','Tank 2 Level','Tank 3 Level','Location','southwest');
g.FontSize = 14;
grid on
axis([20 500 0 0.5])
grid on;
xlabel('Time (s)')
ylabel('Tank 1 Level (m)')
title('Matlab Simulation: Plant Behavior Without Attacks');
matlab2tikz('graficas/tikz/fran_no_attack.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
matlab2tikz('graficas/tikz/std_fran_no_attack.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height', '\figureheight', 'width', '\figurewidth');
 
% Stealth attack without defense
h2=figure(2), 
plot(n,abs_inp_ref(1,1:length(n)),'k--',...
     n,s_attack(1,1:length(n)),'b',...
     n,abs_inp_ref(2,1:length(n)),'k--',...
     n,s_attack(2,1:length(n)),'r',...
     n,s_attack(3,1:length(n)),'m',...
     'LineWidth',2),grid
 
g = legend('Tank 1 Level','Tank 2 Level','Tank 3 Level','Location','southwest');
g.FontSize = 14;
grid on
axis([20 500 0 0.5])
grid on;
xlabel('Time (s)')
ylabel('Tank 1 Level (m)')
title('Matlab Simulation: Plant Behavior With Stealth Attack without Defense');
matlab2tikz('graficas/tikz/fran_diff_no_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
matlab2tikz('graficas/tikz/std_fran_diff_no_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height', '\figureheight', 'width', '\figurewidth');

% Stealth attack with defense
h3=figure(3)
plot(n,abs_inp_ref(1,1:length(n)),'k--',...
     n,s_attack_d(1,1:length(n)),'b',...
     n,abs_inp_ref(2,1:length(n)),'k--',...
     n,s_attack_d(2,1:length(n)),'r',...
     n,s_attack(3,1:length(n)),'m',...
     'LineWidth',2),grid 
 g = legend('Tank 1 Level','Tank 2 Level','Tank 3 Level','Location','southwest');
g.FontSize = 14;
grid on
axis([20 500 0 0.5])
grid on;
xlabel('Time (s)')
ylabel('Tank 1 Level (m)')
title('Matlab Simulation: Plant Behavior With Stealth Attack with Defense');
matlab2tikz('graficas/tikz/fran_diff_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', false, 'height', '\figureheight', 'width', '\figurewidth');
matlab2tikz('graficas/tikz/std_fran_diff_def.tikz', 'showInfo', false, 'parseStrings', false, 'standalone', true, 'height', '\figureheight', 'width', '\figurewidth');


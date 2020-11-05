from . import teste_hipoteses

class hipoteses_t(teste_hipoteses):

    def __init__(self):
        teste_hipoteses.__init__(self)

    def margem_de_erro(self, t_value, desvio_padrao_amostral, n):
        """ 
        Recebe o t-valor, desvio padrão amostral e o número de amostras para calcular o valor da margem de erro.
        """
        return t_value * (desvio_padrao_amostral / (n ** 0.5))

    ## Teste de Hipoteses
    def teste_de_hipoteses(self, n, media_populacional, media_amostral, desvio_padrao_amostral):
        """
        Realiza o teste de hipoteses amostral t.
        """

        # Defina H0 e H1
        H0 = 'H0: u = ' + str(media_populacional)
        if self.tipo_da_hipotese == 'bilateral':
            H1 = 'H1: u != '+ str(media_populacional)
        else:
            H1 = f'H1: u {self.tipo_da_hipotese} '+ str(media_populacional)

        print('Definindo Hipoteses:')
        print(H0)
        print(H1)
        print(f'Confiança: {self.confianca}')
        print(f'Alpha: {self.alpha}')


        # Encontrando estatística do teste
        t = self.calculo_t(media_amostral, media_populacional, desvio_padrao_amostral, n)
        print(f'\nValor de t: {t}')


        print('_____________')

        ##############################
        ## Decisão pela região crítica
        ##############################

        print('\n>>> Decisão pela região crítica\n')
        graus_de_liberdade = n -1
        #t0 = scipy.stats.t.ppf(confianca, graus_de_liberdade)
        t0 = self.t_value(n)
        print('T0 com confiança de', self.confianca,'->', t0)

        print('_____________')

        #######################
        ## Decisão pelo p-valor
        #######################
        print('\n>>> Decisão pelo p-valor\n')
        if t > 0:
            p_value = scipy.stats.t.sf(t, graus_de_liberdade)
        else:
            p_value = scipy.stats.t.sf(t * (-1), graus_de_liberdade)


        if self.tipo_da_hipotese == 'bilateral':
            p_value *= 2
            alpha = self.alpha * 2
        else:
            alpha = self.alpha

        print(f'P Valor do Teste: {p_value}')
        print(f'Valor Alpha: {alpha}')
        print('_____________')

        #########################
        ## Intervalo de Confiânça
        #########################

        print('\n>>> Intervalo de Confiânça\n')
        margem = self.margem_de_erro(t0, desvio_padrao_amostral, n)

        #Calculando intervalo de confiança
        intervalo = self.intervalo_confianca(media_amostral, margem)
        print(f'Intervalo de Confiança: {intervalo}')
        print('_____________')
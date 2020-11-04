class hipoteses_z(teste_hipoteses):

    def __init__(self):
        teste_hipoteses.__init__(self)

    def margem_de_erro(self, z_value, desvio_padrao, n):
        """ 
        Recebe o z-valor, desvio padrão populacional e o número de amostras para calcular o valor da margem de erro.
        """
        return z_value * (desvio_padrao / (n ** 0.5))

    def teste_de_hipoteses(self, n, media_populacional, media_amostral, desvio_padrao):
        """
        Realiza o teste de hipoteses populacional z.
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

        z = self.calculo_z(media_amostral, media_populacional, desvio_padrao, n)
        print(f'\nValor de Z: {z}')

        print('_____________')

        ##############################
        ## Decisão pela região crítica
        ##############################

        print('\n>>> Decisão pela região crítica\n')
        
        # Inputa a probabilidade e ele mostra o Z
        z0 = self.z_value()
        print('Z0 com confiança de', self.confianca,'->', z0)

        print('_____________')

        #######################
        ## Decisão pelo p-valor
        #######################

        print('\n>>> Decisão pelo p-valor\n')
        if z > 0:
            p_value = scipy.stats.norm.sf(z)
        else:
            p_value = scipy.stats.norm.sf(z * (-1))

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
        margem = self.margem_de_erro(z0, desvio_padrao, n)

        #Calculando intervalo de confiança
        intervalo = self.intervalo_confianca(media_amostral, margem)
        print(f'Intervalo de Confiança: {intervalo}')
        print('_____________')
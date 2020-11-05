from . import teste_hipoteses

class hipoteses_proporcao(teste_hipoteses):
    """
    - ME é a margem de erro do estudo.
    - Z é o valor da Distribuição
    Normal que fornece a
    confiança desejada.
    - proporcao_amostral(1 − proporcao_amostral) é a variância estimada que é função de proporcao_amostral fornecido 
    pela amostra piloto.
    - N é o tamanho populacional.
    """

    def __init__(self):
        teste_hipoteses.__init__(self)


    def hipotese(self, proporcao_populacional, proporcao_amostral, n):
        """
        proporcao_populacional é a proporção populacional
        O proporcao_amostral é a proporção amostral 
        n é o tamanho da amostra
        """

        superior = (proporcao_amostral - proporcao_populacional)
        inferior = (proporcao_populacional*(1-proporcao_populacional)) / n

        return superior / (inferior ** 0.5)


    def intervalo_confianca(self, proporcao_amostral, margem_erro):
        return proporcao_amostral - margem_erro, proporcao_amostral + margem_erro

    def margem_de_erro(self, z, proporcao_amostral, n):
        return z * (((proporcao_amostral* (1- proporcao_amostral)) / n) ** 0.5)

    def tamanho_amostral(self, z_value, proporcao_amostral, error_margin):

        return ((z_value ** 2) * (proporcao_amostral * (1 - proporcao_amostral) ) / (error_margin ** 2) )

    def margem_de_erro_finita(self, z_value, proporcao_amostral, n_sample, n_population):

        parte1 = self.proporcao.margem_de_erro(z_value, proporcao_amostral, n_sample)

        ajuste_n = ((n_population - n_sample) / (n_population - 1)) ** 0.5

        return parte1 * ajuste_n

    def tamanho_amostral_finita(self, z_value, proporcao_amostral, error_margin, n_population):

        parte_de_cima = (z_value**2) * (proporcao_amostral * (1 - proporcao_amostral)) * (n_population)
        parte_de_baixo = ((error_margin**2) * (n_population - 1)) + ((z_value**2) * (proporcao_amostral * (1 - proporcao_amostral)))

        return parte_de_cima / parte_de_baixo

    def teste_de_hipoteses(self, proporcao_populacional, proporcao_amostral, n):
        """
        tipo_hipotese => ['bilateral', '>', '<']
        """

        # Defina H0 e H1
        H0 = 'H0: u = ' + str(proporcao_populacional)
        if self.tipo_da_hipotese == 'bilateral':
            H1 = 'H1: u != '+ str(proporcao_populacional)
        else:
            H1 = f'H1: u {self.tipo_da_hipotese} '+ str(proporcao_populacional)

        print('Definindo Hipoteses:')
        print(H0)
        print(H1)

        print(f'Confiança: {self.confianca}')
        print(f'Alpha: {self.alpha}')

        # Encontrando estatística do teste
        z = self.hipotese(proporcao_populacional, proporcao_amostral, n)
        print(f'\nValor de Z: {z}')
        print('_____________')

        ##############################
        ## Decisão pela região crítica
        ##############################

        print('\n>>> Decisão pela região crítica\n')

        # Inputa a probabilidade e ele mostra o Z
        # z0 = st.norm.ppf(confianca)
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

        margem = self.margem_de_erro(z0, proporcao_amostral, n)

        #Calculando intervalo de confiança
        intervalo = self.intervalo_confianca(proporcao_amostral, margem)
        print(f'Intervalo de Confiança: {intervalo}')
        print('_____________')
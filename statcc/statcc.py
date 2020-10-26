class statcc: 

    def __init__(self):

        self.tipo_do_teste = None
        self.tipo_da_hipotese = None 

    ## Margem de erro
    #################

    def cadastrar_teste(self, tipo = 'z'):
        """
        Método para definição de qual será o tipo do teste.

        Pode receber valor 't' para um t-test ou 'z'para um z-test.
        """
        self.tipo_do_teste = tipo

    def cadastrar_hipotese(self, tipo = 'bilateral'):
        """
        Método para definição de qual será o tipo da hipotese, se será unilateral ou bilateral.

        Pode receber valor 't' para um t-test ou 'z'para um z-test.
        """
        self.tipo_da_hipotese = tipo

    def margem_de_erro(self, z_value, desvio_padrao, n):

        margem_erro = z_value * (desvio_padrao / (n ** 0.5))

        return margem_erro

    def margem_de_erro_t(self, t, desvio_padrao_amostral, n):
        """ 
        Trata-se da mesma fórmula de margem de erro, mas com notações diferentes.
        """

        return t * (desvio_padrao_amostral / (n ** 0.5))

    def intervalo_confianca(self, media_amostral, margem_de_erro):
        return media_amostral - margem_de_erro, media_amostral + margem_de_erro


    def tamanho_amostral( z_value, desvio_padrao, error_margin):
        return ((z_value ** 2) * ( desvio_padrao ** 2) / (error_margin ** 2) )

    def margem_de_erro_finita(self, z_value, desvio_padrao, n_sample, n_population):

        parte1 = self.margem_de_erro(z_value, desvio_padrao, n_sample)

        ajuste_n = ((n_population - n_sample) / (n_population - 1)) ** 0.5

        return parte1 * ajuste_n

    def tamanho_amostral_finita(self, z_value, desvio_padrao, error_margin, n_population):

        parte_de_cima = (z_value**2) * (desvio_padrao**2) * (n_population)
        parte_de_baixo = ((error_margin**2) * (n_population - 1)) + ((z_value**2) * (desvio_padrao**2))

        return parte_de_cima / parte_de_baixo

    ## Teste de Hipoteses

    def calculo_z(self, x_barra, media_populacional, desvio_padrao, n):
        return (x_barra - media_populacional) / (desvio_padrao / (n**0.5))

    def calculo_t(self, x_barra, media_populacional, s, n):
        return (x_barra - media_populacional) /( s / (n**0.5))

    def z_value(self, confianca):
        """
        Retorna o valor de Z com base em um nível de confiânça. Tipo indica se valor avaliado é uni ou bilateral.
        
        import scipy.stats as st
        st.norm.ppf()
        """
        if self.tipo_do_teste == 'bilateral':
            alpha = 1 - confianca
            alpha = alpha / 2
            confianca = 1 - alpha
        Z = st.norm.ppf(confianca)

        return Z

    def teste_de_hipoteses(self, n, media_populacional, media_amostral, desvio_padrao, confianca):
        """
        tipo_hipotese => ['bilateral', '>', '<']
        teste => 't ou 'z'
        """

        if self.tipo_do_teste == 't':
            s = desvio_padrao

        # Defina H0 e H1
        H0 = 'H0: u = ' + str(media_populacional)
        if self.tipo_da_hipotese == 'bilateral':
            H1 = 'H1: u != '+ str(media_populacional)
        else:
            H1 = f'H1: u {self.tipo_da_hipotese} '+ str(media_populacional)

        print('Definindo Hipoteses:')
        print(H0)
        print(H1)

        if self.tipo_da_hipotese == 'bilateral':
            alpha = 1 - confianca
            alpha = alpha / 2
            confianca = 1 - alpha
        else:
            alpha = 1 - confianca
        print(f'Confiança: {confianca}')
        print(f'Alpha: {alpha}')


        # Encontrando estatística do teste
        if self.tipo_do_teste == 't':
            t = self.calculo_t(media_amostral, media_populacional, s, n)
            print(f'\nValor de t: {t}')
        else:
            z = self.calculo_z(media_amostral, media_populacional, desvio_padrao, n)
            print(f'\nValor de Z: {z}')


        print('_____________')

        ##############################
        ## Decisão pela região crítica
        ##############################

        print('\n>>> Decisão pela região crítica\n')

        import scipy.stats as st

        if teste == 't':
            graus_de_liberdade = n -1
            t0 = scipy.stats.t.ppf(confianca, graus_de_liberdade)
            print('T0 com confiança de', confianca,'->', t0)
        else:
            # Inputa a probabilidade e ele mostra o Z
            z0 = st.norm.ppf(confianca)
            print('Z0 com confiança de', confianca,'->', z0)

        print('_____________')

        #######################
        ## Decisão pelo p-valor
        #######################

        print('\n>>> Decisão pelo p-valor\n')

        if self.tipo_do_teste == 't':
            if t > 0:
                p_value = scipy.stats.t.sf(t, graus_de_liberdade)
            else:
                p_value = scipy.stats.t.sf(t * (-1), graus_de_liberdade)
        else:
            if z > 0:
                p_value = scipy.stats.norm.sf(z)
            else:
                p_value = scipy.stats.norm.sf(z * (-1))

        if tipo_hipotese == 'bilateral':
            p_value *= 2
            alpha *= 2

        print(f'P Valor do Teste: {p_value}')
        print(f'Valor Alpha: {alpha}')
        print('_____________')

        #########################
        ## Intervalo de Confiânça
        #########################

        print('\n>>> Intervalo de Confiânça\n')

        if self.tipo_do_teste == 't':
            margem = self.margem_de_erro_t(t0, s, n)
        else:
            margem = self.margem_de_erro(z0, desvio_padrao, n)

        #Calculando intervalo de confiança
        intervalo = self.intervalo_confianca(media_amostral, margem)
        print(f'Intervalo de Confiança: {intervalo}')
        print('_____________')

    class proporcao():
        """
        - ME é a margem de erro do estudo.
        - Z é o valor da Distribuição
        Normal que fornece a
        confiança desejada.
        - proporcao_amostral(1 − proporcao_amostral) é a variância estimada que é função de proporcao_amostral fornecido 
        pela amostra piloto.
        - N é o tamanho populacional.
        """
        pass

        def hipotese(proporcao_populacional, proporcao_amostral, n):
            """
            proporcao_populacional é a proporção populacional
            O proporcao_amostral é a proporção amostral 
            n é o tamanho da amostra
            """

            superior = (proporcao_amostral - proporcao_populacional)
            inferior = (proporcao_populacional*(1-proporcao_populacional)) / n

            return superior / (inferior ** 0.5)


        def intervalo_confianca(proporcao_amostral, margem_erro):
            return proporcao_amostral - margem_erro, proporcao_amostral + margem_erro

        def margem_de_erro(z, proporcao_amostral, n):
            temp = (proporcao_amostral* (1- proporcao_amostral)) / n
            me = z * (temp ** 0.5)
            return me

        def tamanho_amostral(z_value, proporcao_amostral, error_margin):

            return ((z_value ** 2) * (proporcao_amostral * (1 - proporcao_amostral) ) / (error_margin ** 2) )

        def margem_de_erro_finita(z_value, proporcao_amostral, n_sample, n_population):

            parte1 = statcc.proporcao.margem_de_erro(z_value, proporcao_amostral, n_sample)

            ajuste_n = ((n_population - n_sample) / (n_population - 1)) ** 0.5

            return parte1 * ajuste_n

        def tamanho_amostral_finita(z_value, proporcao_amostral, error_margin, n_population):

            parte_de_cima = (z_value**2) * (proporcao_amostral * (1 - proporcao_amostral)) * (n_population)
            parte_de_baixo = ((error_margin**2) * (n_population - 1)) + ((z_value**2) * (proporcao_amostral * (1 - proporcao_amostral)))

            return parte_de_cima / parte_de_baixo

        def teste_de_hipoteses(proporcao_populacional, proporcao_amostral, n, confianca, tipo_hipotese):
            """
            tipo_hipotese => ['bilateral', '>', '<']
            """

            # Defina H0 e H1
            H0 = 'H0: u = ' + str(proporcao_populacional)
            if tipo_hipotese == 'bilateral':
                H1 = 'H1: u != '+ str(proporcao_populacional)
            else:
                H1 = f'H1: u {tipo_hipotese} '+ str(proporcao_populacional)

            print('Definindo Hipoteses:')
            print(H0)
            print(H1)

            if tipo_hipotese == 'bilateral':
                alpha = 1 - confianca
                alpha = alpha / 2
                confianca = 1 - alpha
            else:
                alpha = 1 - confianca
            print(f'Confiança: {confianca}')
            print(f'Alpha: {alpha}')

            # Encontrando estatística do teste
            z = statcc.proporcao.hipotese(proporcao_populacional, proporcao_amostral, n)
            print(f'\nValor de Z: {z}')
            print('_____________')

            ##############################
            ## Decisão pela região crítica
            ##############################

            print('\n>>> Decisão pela região crítica\n')

            # Inputa a probabilidade e ele mostra o Z
            z0 = st.norm.ppf(confianca)
            print('Z0 com confiança de', confianca,'->', z0)

            print('_____________')

            #######################
            ## Decisão pelo p-valor
            #######################

            print('\n>>> Decisão pelo p-valor\n')

            if z > 0:
                p_value = scipy.stats.norm.sf(z)
            else:
                p_value = scipy.stats.norm.sf(z * (-1))

            if tipo_hipotese == 'bilateral':
                p_value *= 2
                alpha *= 2

            print(f'P Valor do Teste: {p_value}')
            print(f'Valor Alpha: {alpha}')
            print('_____________')

            #########################
            ## Intervalo de Confiânça
            #########################

            print('\n>>> Intervalo de Confiânça\n')

            margem = statcc.proporcao.margem_de_erro(z0, proporcao_amostral, n)

            #Calculando intervalo de confiança
            intervalo = statcc.proporcao.intervalo_confianca(proporcao_amostral, margem)
            print(f'Intervalo de Confiança: {intervalo}')
            print('_____________')
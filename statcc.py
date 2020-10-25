class statcc:

    def __init__(self):

        pass

    ## Margem de erro
    #################

    def margem_de_erro( z_value, std, n):

        margem_erro = z_value * (std / (n ** 0.5))

        return margem_erro

    def margem_de_erro_t( t, std_amostral, n):
        """ 
        Trata-se da mesma fórmula de margem de erro, mas com notações diferentes.
        """

        margem_erro = t * (std_amostral / (n ** 0.5))

        return margem_erro

    def intervalo_confianca( x, margem_de_erro):
        return x - margem_de_erro, x + margem_de_erro


    def tamanho_amostral( z_value, std, error_margin):

        n = ((z_value ** 2) * ( std ** 2) / (error_margin ** 2) )

        return n

    def margem_de_erro_finita( z_value, std, n_sample, n_population):

        parte1 = self.margem_de_erro(z_value, std, n_sample)

        ajuste_n = ((n_population - n_sample) / (n_population - 1)) ** 0.5

        return parte1 * ajuste_n

    def tamanho_amostral_finita( z_value, std, error_margin, n_population):

        parte_de_cima = (z_value**2) * (std**2) * (n_population)
        parte_de_baixo = ((error_margin**2) * (n_population - 1)) + ((z_value**2) * (std**2))

        return parte_de_cima / parte_de_baixo

    ## Teste de Hipoteses

    def calculo_z( x_barra, u, std, n):
        return (x_barra - u) / (std / (n**0.5))

    def calculo_t( x_barra, u, s, n):
        return (x_barra - u) /( s / (n**0.5))

    def z_value( confianca, tipo = 'unilateral'):
        """
        Retorna o valor de Z com base em um nível de confiânça. Tipo indica se valor avaliado é uni ou bilateral.
        
        import scipy.stats as st
        st.norm.ppf()
        """
        if tipo == 'bilateral':
            alpha = 1 - confianca
            alpha = alpha / 2
            confianca = 1 - alpha
        Z = st.norm.ppf(confianca)

        return Z

    def teste_de_hipoteses( n, u, x, std, confianca, tipo_hipotese, teste):
        """
        tipo_hipotese => ['bilateral', '>', '<']
        teste => 't ou 'z'
        """

        if teste == 't':
            s = std

        # Defina H0 e H1
        H0 = 'H0: u = ' + str(u)
        if tipo_hipotese == 'bilateral':
            H1 = 'H1: u != '+ str(u)
        else:
            H1 = f'H1: u {tipo_hipotese} '+ str(u)

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
        if teste == 't':
            t = calculo_t(x, u, s, n)
            print(f'\nValor de t: {t}')
        else:
            z = calculo_z(x, u, std, n)
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

        if teste == 't':
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

        if teste == 't':
            margem = margem_de_erro_t(t0, s, n)
        else:
            margem = margem_de_erro(z0, std, n)

        #Calculando intervalo de confiança
        intervalo = intervalo_confianca(x, margem)
        print(f'Intervalo de Confiança: {intervalo}')
        print('_____________')

    class proporcao():
        """
        - ME é a margem de erro do estudo.
        - Z é o valor da Distribuição
        Normal que fornece a
        confiança desejada.
        - p_barra(1 − p_barra) é a variância estimada que é função de p_barra fornecido 
        pela amostra piloto.
        - N é o tamanho populacional.
        """
        pass

        def hipotese(p, p_barra, n):
            """
            p é a proporção populacional
            O p_barra é a proporção amostral
            n é o tamanho da amostra
            """

            superior = (p_barra - p)
            inferior = (p*(1-p)) / n

            return superior / (inferior ** 0.5)


        def intervalo_confianca(p_barra, me):
            return p_barra - me, p_barra + me

        def margem_de_erro(z, p_barra, n):
            temp = (p_barra* (1- p_barra)) / n
            me = z * (temp ** 0.5)
            return me

        def tamanho_amostral(z_value, p_barra, error_margin):

            n = ((z_value ** 2) * (p_barra * (1 - p_barra) ) / (error_margin ** 2) )

            return n

        def margem_de_erro_finita(z_value, p_barra, n_sample, n_population):

            parte1 = statcc.proporcao.margem_de_erro(z_value, p_barra, n_sample)

            ajuste_n = ((n_population - n_sample) / (n_population - 1)) ** 0.5

            return parte1 * ajuste_n

        def tamanho_amostral_finita(z_value, p_barra, error_margin, n_population):

            parte_de_cima = (z_value**2) * (p_barra * (1 - p_barra)) * (n_population)
            parte_de_baixo = ((error_margin**2) * (n_population - 1)) + ((z_value**2) * (p_barra * (1 - p_barra)))

            return parte_de_cima / parte_de_baixo

        def teste_de_hipoteses(p, p_barra, n, confianca, tipo_hipotese):
            """
            tipo_hipotese => ['bilateral', '>', '<']
            """

            # Defina H0 e H1
            H0 = 'H0: u = ' + str(p)
            if tipo_hipotese == 'bilateral':
                H1 = 'H1: u != '+ str(p)
            else:
                H1 = f'H1: u {tipo_hipotese} '+ str(p)

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
            z = statcc.proporcao.hipotese(p, p_barra, n)
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

            margem = statcc.proporcao.margem_de_erro(z0, p_barra, n)

            #Calculando intervalo de confiança
            intervalo = statcc.proporcao.intervalo_confianca(p_barra, margem)
            print(f'Intervalo de Confiança: {intervalo}')
            print('_____________')
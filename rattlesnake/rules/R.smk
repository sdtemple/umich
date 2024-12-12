rule R:
    input:
        linuxfile='{folder}/linuxfile{numeric}.txt'
    output:
        Rfile='{folder}/Rfile{numeric}.txt'
    shell:
        """
        Rscript scripts/greetings.R {output.Rfile}
        """

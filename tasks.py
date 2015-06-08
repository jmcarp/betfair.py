# -*- coding: utf-8 -*-

from invoke import task, run


DEFAULT_NAME = 'certs/betfair'
DEFAULT_BITS = 2048


@task
def generate_key(name=DEFAULT_NAME, bits=DEFAULT_BITS):
    key_file = '{0}.key'.format(name)
    cmd = 'openssl genrsa -out {0} {1}'.format(key_file, bits)
    run(cmd)


@task
def generate_cert(name=DEFAULT_NAME):
    key_file = '{0}.key'.format(name)
    csr_file = '{0}.csr'.format(name)
    cmd = 'openssl req -new -key {0} -out {1}'.format(key_file, csr_file)
    run(cmd)


@task
def sign_cert(name=DEFAULT_NAME):
    key_file = '{0}.key'.format(name)
    csr_file = '{0}.csr'.format(name)
    crt_file = '{0}.crt'.format(name)
    cmd = 'openssl x509 -req -signkey {0} -in {1} -out {2}'.format(
        key_file,
        csr_file,
        crt_file,
    )
    run(cmd)


@task
def generate_pem(name=DEFAULT_NAME):
    key_file = '{0}.key'.format(name)
    crt_file = '{0}.crt'.format(name)
    pem_file = '{0}.pem'.format(name)
    cmd = 'cat {0} {1} > {2}'.format(crt_file, key_file, pem_file)
    run(cmd)


@task
def ssl(name=DEFAULT_NAME, bits=DEFAULT_BITS):
    generate_key(name, bits)
    generate_cert(name)
    sign_cert(name)
    generate_pem(name)

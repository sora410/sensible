# coding: utf-8

import glob
import os.path
import subprocess
import sys

me = sys.argv[0]
parent = 'exts'

class RunCommandError(Exception):
	pass

def print_inline(t): print(t, end='', flush=True)

def _mkdir(dirname, is_parents=False):
	if not is_parents: dirname = parent + '/' + dirname
	if os.path.exists(dirname): return
	message = 'making %s(parent)...' if is_parents else 'making %s...' 
	print_inline(message % dirname)
	try:
		subprocess.call(['mkdir', '-p', dirname])
	except subprocess.CalledProcessError:
		raise RunCommandError('at \'mkdir\'')
	print('ok')

def _mv(filename, ext):
	print_inline('transferring %s...' % filename)
	try:
		subprocess.call(['mv', filename, parent+'/'+ext])
	except subprocess.CalledProcessError:
		raise RunCommandError('at \'mv\'')
	print('ok')

def _ls(dirname=None):
	command = 'ls' if dirname is None else ['ls', dirname]
	try:
		return subprocess.check_output(command)
	except subprocess.CalledProcessError:
		raise RunCommandError('at \'ls\'')

def _rm(dirname):
	print_inline('removing /%s...' % dirname)
	try:
		subprocess.call(['rm', '-rf', dirname])
	except subprocess.CalledProcessError:
		raise RunCommandError('at \'rm\'')
	print('ok')

def is_empty(dirname):
	return True if not _ls(dirname) else False

def cleanup():
	# remove nomeaning directory for sensible.py
	if is_empty(parent+'/py'):
		_rm(parent+'/py')

def _gather_file_extensions():
	print_inline('gathering file extensions...')
	lsf = _ls().decode('utf-8').split('\n')
	for f in lsf:
		_, ext = os.path.splitext(f)
		if not ext: continue
		yield ext
	print('ok')

def grouping():
	_mkdir(parent, is_parents=True)
	exts = {ext.strip('.') for ext in _gather_file_extensions()}
	for ext in exts:
		_mkdir(ext)
		for filename in glob.glob('*.'+ext):
			if filename == me: continue 
			_mv(filename, ext)
	cleanup()

if __name__ == '__main__':
	grouping()
	print('done.')

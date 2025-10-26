import unittest
import os
import shutil
import tempfile
from copystatic import copy_files_recursive


class TestCopyStatic(unittest.TestCase):
    def setUp(self):
        """Cria diretórios temporários para teste"""
        self.test_dir = tempfile.mkdtemp()
        self.source_dir = os.path.join(self.test_dir, "source")
        self.dest_dir = os.path.join(self.test_dir, "dest")
        
        # Cria estrutura de teste
        os.makedirs(self.source_dir)
    
    def tearDown(self):
        """Remove diretórios temporários após teste"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_copy_simple_files(self):
        """Testa cópia de arquivos simples"""
        # Cria arquivos de teste
        with open(os.path.join(self.source_dir, "file1.txt"), "w") as f:
            f.write("content1")
        with open(os.path.join(self.source_dir, "file2.txt"), "w") as f:
            f.write("content2")
        
        # Executa cópia
        copy_files_recursive(self.source_dir, self.dest_dir)
        
        # Valida
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "file1.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "file2.txt")))
        
        with open(os.path.join(self.dest_dir, "file1.txt")) as f:
            self.assertEqual(f.read(), "content1")
    
    def test_copy_nested_directories(self):
        """Testa cópia recursiva de diretórios aninhados"""
        # Cria estrutura aninhada
        nested_dir = os.path.join(self.source_dir, "level1", "level2", "level3")
        os.makedirs(nested_dir)
        
        with open(os.path.join(self.source_dir, "root.txt"), "w") as f:
            f.write("root")
        with open(os.path.join(self.source_dir, "level1", "l1.txt"), "w") as f:
            f.write("level1")
        with open(os.path.join(nested_dir, "deep.txt"), "w") as f:
            f.write("deep")
        
        # Executa cópia
        copy_files_recursive(self.source_dir, self.dest_dir)
        
        # Valida estrutura
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "root.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "level1", "l1.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "level1", "level2", "level3", "deep.txt")))
        
        with open(os.path.join(self.dest_dir, "level1", "level2", "level3", "deep.txt")) as f:
            self.assertEqual(f.read(), "deep")
    
    def test_clears_existing_destination(self):
        """Testa que o destino é limpo antes da cópia"""
        # Cria arquivo no destino
        os.makedirs(self.dest_dir)
        old_file = os.path.join(self.dest_dir, "old.txt")
        with open(old_file, "w") as f:
            f.write("should be deleted")
        
        # Cria novo arquivo na fonte
        with open(os.path.join(self.source_dir, "new.txt"), "w") as f:
            f.write("new content")
        
        # Deletar destino antes de copiar (como no main.py)
        if os.path.exists(self.dest_dir):
            shutil.rmtree(self.dest_dir)
        
        # Executa cópia
        copy_files_recursive(self.source_dir, self.dest_dir)
        
        # Valida que arquivo antigo foi deletado
        self.assertFalse(os.path.exists(old_file))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, "new.txt")))
    
    def test_empty_source_directory(self):
        """Testa cópia de diretório vazio"""
        copy_files_recursive(self.source_dir, self.dest_dir)
        
        # Destino deve existir mas estar vazio
        self.assertTrue(os.path.exists(self.dest_dir))
        self.assertEqual(len(os.listdir(self.dest_dir)), 0)


if __name__ == "__main__":
    unittest.main()

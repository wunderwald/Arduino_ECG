const fs = require('fs');
const writeJSON = require('./writeJSON');

//leaf := a directory with no subdirectories
const isLeaf = dir => {
    const ls = fs.readdirSync(dir);
    return ls.every(item => fs.lstatSync(`${dir}/${item}`).isFile());
}

const discoverFilesRecursive = (currentDir, fileType) => {
    const dirIsLeaf = isLeaf(currentDir);

    //if dir is a leaf return list of files that end with fileType
    if(dirIsLeaf){
        const files = fs.readdirSync(currentDir)
            .filter(file => file.endsWith(fileType))
            .map(file => `${currentDir}/${file}`);
        return files;
    }
    //if dir is a node, discover files in all subdirectories
    else{
        const files = [];
        const subDirs = fs.readdirSync(currentDir)
            .filter(item => fs.lstatSync(`${currentDir}/${item}`).isDirectory())
            .map(subDir => `${currentDir}/${subDir}`);
        subDirs.forEach(subDir => {
            files.push(...discoverFilesRecursive(subDir,  fileType));
        });
        return files;
    }
}

const folderStructure = (dir, fileType) => {
    //first, read all "subject" directories
    const subjectDirs = fs.readdirSync(dir)
        .filter(item => fs.lstatSync(`${dir}/${item}`).isDirectory)
        .filter(subDir => subDir.startsWith('subject_'))
        .map(subDir => ({ 
            path: `${dir}/${subDir}`,
            title: subDir, 
            trials: [] 
        }));
    
    //then, read all 'trial' files in each 'subject dir 
    const structure = subjectDirs.map(subjectDirObject => {
        const subjectDir = subjectDirObject.path;
        
        const trials = fs.readdirSync(subjectDir)
            .filter(o => fs.lstatSync(`${subjectDir}/${o}`).isFile())
            .filter(file => file.includes('trial_'))
            .map(file => Object({
                title: file.substring(0, file.length - '.json'.length),
                file: file
            }));
        
        subjectDirObject.trials.push(...trials);
        return subjectDirObject;
    });

    return structure;

};

module.exports = (dir, fileType) => {
    //list all files of fileType
    const files = discoverFilesRecursive(dir, fileType);
    
    //reproduce the folder structure
    const structure = folderStructure(dir, fileType);

    //create and write registry
    const registry = { paths: files, hierarchy: { files: structure } };
    const registryPath = `${dir}/registry.json`;
    writeJSON(registry, registryPath);
}
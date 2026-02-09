
const fs = require('fs');
const path = require('path');

// Base paths
const PROJECT_ROOT = '/home/irisso/proyectos/facturacion';
const FRONTEND_SRC = path.join(PROJECT_ROOT, 'frontend/src');

// Mappings
const ALIASES = {
    '@shared': path.join(FRONTEND_SRC, 'shared'),
    '@modules': path.join(FRONTEND_SRC, 'modules')
};

// Known routes from previous stage (hardcoded for simplicity or read from json)
const ROUTES_JSON_PATH = '/home/irisso/proyectos/facturacion/.artifacts/requests/REQ-FUNC-003/architecture/routes_check.json';
const ROUTES = JSON.parse(fs.readFileSync(ROUTES_JSON_PATH, 'utf8'));

function analyzeFile(filePath) {
    if (!fs.existsSync(filePath)) return null;
    const content = fs.readFileSync(filePath, 'utf8');

    return {
        hasTable: content.includes('<table') || content.includes('DataTable') || content.includes('v-for'),
        hasForm: content.includes('<form') || content.includes('Input') || content.includes('v-model'),
        hasApi: content.includes('axios') || content.includes('service') || content.includes('fetch'),
        hasUseCrud: content.includes('useCrud'),
        isList: filePath.includes('List') || filePath.includes('Tree'),
        isCreate: filePath.includes('Create') || filePath.includes('New'),
        isEdit: filePath.includes('Edit') || filePath.includes('Modify'),
        isDetail: filePath.includes('Detail') || filePath.includes('View'), // 'View' is generic, often list+form
        imports: (content.match(/import .* from .*/g) || []).join('\n')
    };
}

function detectCrud() {
    console.log('Detecting CRUD...');
    const matrix = [];
    const missing = [];

    ROUTES.forEach(route => {
        const analysis = analyzeFile(route.resolvedPath);
        if (!analysis) return;

        let type = 'Unknown';
        if (analysis.isList) type = 'List';
        if (analysis.isCreate) type = 'Create';
        if (analysis.isEdit) type = 'Update';
        if (analysis.isDetail && !analysis.isList) type = 'Detail';
        if (route.path.includes('nuevo')) type = 'Create';

        // Maestros often use a single View for CRUD
        if (route.component.includes('Maestros') && route.component.includes('View')) {
            type = 'CRUD (Single View)';
        }

        matrix.push({
            path: route.path,
            component: route.component,
            type: type,
            features: {
                table: analysis.hasTable,
                form: analysis.hasForm,
                api: analysis.hasApi,
                useCrud: analysis.hasUseCrud
            }
        });

        // Simple heuristic for missing operations
        if (type === 'List' && !analysis.hasApi && !analysis.hasUseCrud) {
            missing.push({ path: route.path, issue: 'List view without explicit API usage or useCrud' });
        }
    });

    fs.writeFileSync('/home/irisso/proyectos/facturacion/.artifacts/requests/REQ-FUNC-003/ui/crud_matrix_data.json', JSON.stringify(matrix, null, 2));
    fs.writeFileSync('/home/irisso/proyectos/facturacion/.artifacts/requests/REQ-FUNC-003/ui/missing_ops_data.json', JSON.stringify(missing, null, 2));
    console.log('CRUD detection complete.');
}

detectCrud();

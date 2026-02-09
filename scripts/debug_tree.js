
// Mock data based on expected DB content
const mockItems = [
    { id: 1, nombre: 'Maestros', path: null, parent_id: null, roles: [] }, // Parent
    { id: 4, nombre: 'Puntos de Venta', path: '/puntos-venta', parent_id: 1, roles: [] } // Child
];

const buildTree = (items) => {
    const map = new Map();
    const roots = [];

    // 1. Create nodes
    items.forEach(item => {
        map.set(item.id, {
            id: item.id,
            label: item.nombre,
            route: item.path,
            children: []
        });
    });

    // 2. Assemble tree
    items.forEach(item => {
        const node = map.get(item.id);
        console.log(`Processing ${item.nombre} (ID: ${item.id}, Parent: ${item.parent_id})`);

        if (item.parent_id && map.has(item.parent_id)) {
            const parent = map.get(item.parent_id);
            console.log(`-> Adding to parent ${parent.label}`);
            parent.children.push(node);
        } else {
            console.log(`-> Adding to roots`);
            roots.push(node);
        }
    });

    return roots;
};

const tree = buildTree(mockItems);
console.log(JSON.stringify(tree, null, 2));

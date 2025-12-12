// 从JSON文件加载数据的函数
async function loadData() {
    try {
        // 加载文献数据
        const literatureResponse = await fetch('literature.json');
        const literatureData = await literatureResponse.json();

        // 加载分类数据
        const taxonomyResponse = await fetch('taxonomy.json');
        const taxonomyData = await taxonomyResponse.json();

        // 加载样本数据
        const sampleResponse = await fetch('sample.json');
        const sampleData = await sampleResponse.json();

        // 将数据存储在全局变量中
        window.sampleData = {
            literature: literatureData,
            taxonomy: taxonomyData,
            samples: sampleData
        };

        console.log('数据加载成功');
        return window.sampleData;
    } catch (error) {
        console.error('加载数据时出错:', error);
        // 如果无法加载真实数据，则使用示例数据
        window.sampleData = {
            literature: [
                {
                    "id": "LIT001",
                    "title": "A new species of butterfly from Amazon rainforest",
                    "authors": "Smith, J.; Johnson, A.",
                    "journal": "Journal of Insect Taxonomy",
                    "year": "2023",
                    "doi": "10.1234/jit.2023.001",
                    "url": "https://example.com/papers/LIT001",
                    "abstract": "This paper describes a new species of butterfly discovered in the Amazon rainforest. The species belongs to the family Nymphalidae and is characterized by its distinctive wing coloration."
                },
                {
                    "id": "LIT002",
                    "title": "Revision of the genus Panthera in Asia",
                    "authors": "Brown, T.; Davis, M.",
                    "journal": "Mammalian Biology",
                    "year": "2022",
                    "doi": "10.5678/mb.2022.002",
                    "url": "https://example.com/papers/LIT002",
                    "abstract": "A comprehensive revision of the genus Panthera in Asia, including morphological analysis and phylogenetic relationships of various subspecies."
                }
            ],
            taxonomy: [
                {
                    "id": "TAX001",
                    "name": "Amazonia papilionis",
                    "level": "Species",
                    "type": "new taxon",
                    "lit_id": "LIT001",
                    "parent_tax_id": "",
                    "description": "A newly discovered butterfly species from the Amazon basin. Distinguished by iridescent blue wings with orange borders."
                },
                {
                    "id": "TAX002",
                    "name": "Panthera tigris altaica",
                    "level": "Species",
                    "type": "new combination",
                    "lit_id": "LIT002",
                    "parent_tax_id": "TAX003",
                    "description": "The Siberian tiger, also known as the Amur tiger, is a tiger population in the Russian Far East and Northeast China."
                },
                {
                    "id": "TAX003",
                    "name": "Panthera tigris",
                    "level": "Species",
                    "type": "new taxon",
                    "lit_id": "LIT002",
                    "parent_tax_id": "",
                    "description": "The tiger is the largest extant cat species and a member of the genus Panthera."
                }
            ],
            samples: [
                {
                    "id": "SMP001",
                    "tax_id": "TAX001",
                    "collector": "Dr. Smith",
                    "latitude": 3.456789,
                    "longitude": -60.123456,
                    "description": "Collected from the canopy of primary rainforest at the type locality."
                },
                {
                    "id": "SMP002",
                    "tax_id": "TAX002",
                    "collector": "Dr. Brown",
                    "latitude": 45.678912,
                    "longitude": 120.345678,
                    "description": "Specimen collected during winter tracking expedition in the Sikhote-Alin mountain range."
                }
            ]
        };
        return window.sampleData;
    }
}

// 初始化数据加载
loadData();
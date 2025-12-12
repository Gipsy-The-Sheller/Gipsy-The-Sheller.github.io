const { createApp, ref, computed, onMounted } = Vue;

createApp({
    setup() {
        const activeTab = ref('literature');
        const literatureSearch = ref('');
        const taxonomySearch = ref('');
        const sampleSearch = ref('');
        const loading = ref(false);
        const selected_item = ref(null);
        const selected_item_type = ref('');
        
        // 数据存储
        const literatureData = ref([]);
        const taxonomyData = ref([]);
        const sampleData = ref([]);

        const tabs = [
            { id: 'literature', name: '文献 (LITid)' },
            { id: 'taxonomy', name: '分类 (TAXid)' },
            { id: 'samples', name: '样本 (SMPid)' },
            { id: 'about', name: '关于' }
        ];

        // 等待数据加载完成
        const waitForData = () => {
            return new Promise(resolve => {
                const checkData = () => {
                    if (window.sampleData) {
                        resolve(window.sampleData);
                    } else {
                        setTimeout(checkData, 100);
                    }
                };
                checkData();
            });
        };

        // 初始化数据
        const initData = async () => {
            try {
                loading.value = true;
                await waitForData();
                literatureData.value = window.sampleData.literature || [];
                taxonomyData.value = window.sampleData.taxonomy || [];
                sampleData.value = window.sampleData.samples || [];
            } catch (error) {
                console.error('初始化数据出错:', error);
            } finally {
                loading.value = false;
            }
        };

        // 搜索算法实现
        const searchInData = (data, searchTerm, fields) => {
            if (!searchTerm) return data;
            
            const term = searchTerm.toLowerCase();
            return data.filter(item => {
                return fields.some(field => {
                    const value = item[field];
                    if (value === undefined || value === null) return false;
                    return value.toString().toLowerCase().includes(term);
                });
            });
        };

        // 获取文献数据
        const fetchLiterature = async () => {
            try {
                loading.value = true;
                await waitForData();
                // 使用本地数据和搜索算法
                literatureData.value = searchInData(
                    window.sampleData.literature || [], 
                    literatureSearch.value,
                    ['id', 'title', 'authors', 'journal', 'year', 'doi', 'abstract']
                );
            } catch (error) {
                console.error('处理文献数据出错:', error);
            } finally {
                loading.value = false;
            }
        };

        // 获取分类数据
        const fetchTaxonomy = async () => {
            try {
                loading.value = true;
                await waitForData();
                // 使用本地数据和搜索算法
                taxonomyData.value = searchInData(
                    window.sampleData.taxonomy || [], 
                    taxonomySearch.value,
                    ['id', 'name', 'level', 'type', 'lit_id', 'description']
                );
            } catch (error) {
                console.error('处理分类数据出错:', error);
            } finally {
                loading.value = false;
            }
        };

        // 获取样本数据
        const fetchSamples = async () => {
            try {
                loading.value = true;
                await waitForData();
                // 使用本地数据和搜索算法
                sampleData.value = searchInData(
                    window.sampleData.samples || [], 
                    sampleSearch.value,
                    ['id', 'tax_id', 'collector', 'latitude', 'longitude', 'description']
                );
            } catch (error) {
                console.error('处理样本数据出错:', error);
            } finally {
                loading.value = false;
            }
        };

        // 生成ID（仅用于演示，实际部署时需要后端支持）
        const generateId = (type) => {
            // 这里只是一个模拟的ID生成器
            const prefix = type === 'literature' ? 'LIT' : type === 'taxonomy' ? 'TAX' : 'SMP';
            return `${prefix}-${Math.random().toString(36).substr(2, 9)}`;
        };

        // 初始化数据获取
        onMounted(async () => {
            await initData();
            await fetchLiterature();
            await fetchTaxonomy();
            await fetchSamples();
        });

        // 监听搜索变化
        const onLiteratureSearch = () => {
            fetchLiterature();
        };

        const onTaxonomySearch = () => {
            fetchTaxonomy();
        };

        const onSampleSearch = () => {
            fetchSamples();
        };

        // 选中项目
        const selectItem = (item, type) => {
            selected_item.value = item;
            selected_item_type.value = type;
        };

        // 取消选中项目
        const deselectItem = () => {
            selected_item.value = null;
            selected_item_type.value = '';
        };

        // 过滤后的数据
        const filteredLiterature = computed(() => {
            return literatureData.value;
        });

        const filteredTaxonomy = computed(() => {
            return taxonomyData.value;
        });

        const filteredSamples = computed(() => {
            return sampleData.value;
        });

        return {
            activeTab,
            tabs,
            literatureSearch,
            taxonomySearch,
            sampleSearch,
            loading,
            selected_item,
            selected_item_type,
            filteredLiterature,
            filteredTaxonomy,
            filteredSamples,
            onLiteratureSearch,
            onTaxonomySearch,
            onSampleSearch,
            selectItem,
            deselectItem,
            generateId
        };
    }
}).mount('#app');
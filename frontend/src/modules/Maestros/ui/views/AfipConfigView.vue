
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { httpClient as api } from '@/shared/http/client'

interface CertInfo {
  status: string
  subject?: string
  issuer?: string
  valid_from?: string
  valid_to?: string
  days_remaining?: number
  production?: boolean
  error?: string
  path?: string
}

const certInfo = ref<CertInfo | null>(null)
const loading = ref(false)
const uploading = ref(false)
const error = ref('')
const successMessage = ref('')

// File inputs
const certFile = ref<File | null>(null)
const keyFile = ref<File | null>(null)

const fetchStatus = async () => {
  loading.value = true
  try {
    const res = await api.get('/config/afip/certs')
    certInfo.value = res.data
  } catch (err: any) {
    error.value = "Error cargando estado: " + (err.response?.data?.detail || err.message)
  } finally {
    loading.value = false
  }
}

const handleCertUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
      certFile.value = file
  }
}

const handleKeyUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
      keyFile.value = file
  }
}

const uploadCredentials = async () => {
  if (!certFile.value || !keyFile.value) {
    alert("Debe seleccionar ambos archivos (.crt y .key)")
    return
  }
  
  uploading.value = true
  error.value = ''
  successMessage.value = ''
  
  const formData = new FormData()
  formData.append('cert_file', certFile.value)
  formData.append('key_file', keyFile.value)
  
  try {
    const res = await api.post('/config/afip/certs', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    successMessage.value = res.data.message
    await fetchStatus()
    certFile.value = null
    keyFile.value = null
  } catch (err: any) {
    error.value = "Error subiendo credenciales: " + (err.response?.data?.detail || err.message)
  } finally {
    uploading.value = false
  }
}

onMounted(() => {
  fetchStatus()
})
</script>

<template>
    <div class="px-4 sm:px-6 lg:px-8 py-8">
      <div class="sm:flex sm:items-center">
        <div class="sm:flex-auto">
          <h1 class="text-xl font-semibold text-gray-900">Configuración AFIP</h1>
          <p class="mt-2 text-sm text-gray-700">Gestión de certificados digitales y credenciales de acceso.</p>
        </div>
      </div>
      
      <!-- Status Card -->
      <div class="mt-8 bg-white overflow-hidden shadow rounded-lg border border-gray-200">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900">Estado del Certificado Actual</h3>
          
          <div v-if="loading" class="mt-4 text-gray-500">Cargando información...</div>

          <div v-else-if="error" class="mt-4 rounded-md bg-red-50 p-4">
              <h3 class="text-sm font-medium text-red-800">Error cargando estado</h3>
              <p class="mt-1 text-sm text-red-700">{{ error }}</p>
          </div>
          
          <div v-else-if="certInfo" class="mt-4">
            <div v-if="certInfo.status === 'missing'" class="rounded-md bg-red-50 p-4">
              <div class="flex">
                <div class="ml-3">
                  <h3 class="text-sm font-medium text-red-800">No se encontró certificado</h3>
                  <div class="mt-2 text-sm text-red-700">
                    <p>Ruta esperada: {{ certInfo.path }}</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else-if="certInfo.status === 'error'" class="rounded-md bg-red-50 p-4">
               <p class="text-red-700">Error leyendo certificado: {{ certInfo.error }}</p>
            </div>
            
            <dl v-else class="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-2">
              <div class="sm:col-span-1">
                <dt class="text-sm font-medium text-gray-500">Subject (Titular)</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ certInfo.subject }}</dd>
              </div>
              <div class="sm:col-span-1">
                <dt class="text-sm font-medium text-gray-500">Issuer (Emisor)</dt>
                <dd class="mt-1 text-sm text-gray-900">{{ certInfo.issuer }}</dd>
              </div>
              <div class="sm:col-span-1">
                <dt class="text-sm font-medium text-gray-500">Entorno</dt>
                <dd class="mt-1 text-sm font-bold" :class="certInfo.production ? 'text-green-600' : 'text-yellow-600'">
                  {{ certInfo.production ? 'PRODUCCIÓN' : 'HOMOLOGACIÓN / TESTING' }}
                </dd>
              </div>
              <div class="sm:col-span-1">
                <dt class="text-sm font-medium text-gray-500">Vigencia</dt>
                <dd class="mt-1 text-sm text-gray-900" v-if="certInfo.valid_from && certInfo.valid_to">
                  {{ new Date(certInfo.valid_from).toLocaleDateString() }} - {{ new Date(certInfo.valid_to).toLocaleDateString() }}
                </dd>
              </div>
              <div class="sm:col-span-2" v-if="certInfo.days_remaining !== undefined">
                 <div class="rounded-md p-4" :class="{
                    'bg-green-50': certInfo.days_remaining > 30,
                    'bg-yellow-50': certInfo.days_remaining <= 30 && certInfo.days_remaining > 7,
                    'bg-red-50': certInfo.days_remaining <= 7
                 }">
                    <p class="text-sm font-bold" :class="{
                       'text-green-700': certInfo.days_remaining > 30,
                       'text-yellow-700': certInfo.days_remaining <= 30 && certInfo.days_remaining > 7,
                       'text-red-700': certInfo.days_remaining <= 7
                    }">
                       Días restantes: {{ certInfo.days_remaining }}
                    </p>
                 </div>
              </div>
            </dl>
          </div>
        </div>
      </div>
      
      <!-- Upload Form -->
      <div class="mt-8 bg-white overflow-hidden shadow rounded-lg border border-gray-200">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900">Actualizar Credenciales</h3>
          <p class="mt-1 max-w-2xl text-sm text-gray-500">
            Suba los archivos proporcionados por AFIP. La clave privada (.key) se almacena de forma segura.
          </p>
          
          <div class="mt-6 grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
            <div class="sm:col-span-3">
              <label for="cert-file" class="block text-sm font-medium text-gray-700">Certificado (.crt)</label>
              <div class="mt-1">
                <input type="file" id="cert-file" accept=".crt" @change="handleCertUpload" 
                       class="block w-full text-sm text-slate-500
                        file:mr-4 file:py-2 file:px-4
                        file:rounded-full file:border-0
                        file:text-sm file:font-semibold
                        file:bg-blue-50 file:text-blue-700
                        hover:file:bg-blue-100" />
              </div>
            </div>
            
            <div class="sm:col-span-3">
              <label for="key-file" class="block text-sm font-medium text-gray-700">Clave Privada (.key)</label>
               <div class="mt-1">
                <input type="file" id="key-file" accept=".key" @change="handleKeyUpload"
                       class="block w-full text-sm text-slate-500
                        file:mr-4 file:py-2 file:px-4
                        file:rounded-full file:border-0
                        file:text-sm file:font-semibold
                        file:bg-blue-50 file:text-blue-700
                        hover:file:bg-blue-100" />
              </div>
            </div>
          </div>
          
          <div class="mt-6">
             <button @click="uploadCredentials" :disabled="uploading"
                class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50">
                {{ uploading ? 'Subiendo...' : 'Actualizar Credenciales' }}
             </button>
          </div>
          
          <div v-if="successMessage" class="mt-4 rounded-md bg-green-50 p-4">
             <p class="text-sm text-green-700">{{ successMessage }}</p>
          </div>
          <div v-if="error" class="mt-4 rounded-md bg-red-50 p-4">
             <p class="text-sm text-red-700">{{ error }}</p>
          </div>
          
        </div>
      </div>
  </div>
</template>

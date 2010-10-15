def ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
          def get(self, resource):
              resource = str(urllib.unquote(resource))
              blob_info = blobstore.BlobInfo.get(resource)
              self.send_blob(blob_info)
      
      def main():
              application = webapp.WSGIApplication(
                                              [('/upload_sermon', MainHandler),
                                              ('/upload', UploadHandler),
                                              ('/serve/([^/]+)?', ServeHandler), #
                                              ], debug=True)
              run_wsgi_app(application)
      
     if __name__ == '__main__':
              main()
